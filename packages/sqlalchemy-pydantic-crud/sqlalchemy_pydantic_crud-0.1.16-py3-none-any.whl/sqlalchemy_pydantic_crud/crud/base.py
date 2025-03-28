import logging
from collections import defaultdict
from collections.abc import Sequence
from typing import Type, Generic

from sqlalchemy import (
    select,
    inspect,
    Select,
    asc,
    desc,
    delete,
    text,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, contains_eager, RelationshipProperty

from .helpers import (
    update_rows,
    prepare_where_clause,
    instance_to_model,
    prepare_update_data, get_record_count,
)
from .decorators import session_manager, autologger
from ..interface.crud import (
    BaseCrudInterface,
    BaseDbModelType,
    BaseSchemaType, SchemaType,
)


from ..interface.session import SessionProviderInterface
from ..models.schema import BaseSchema


logger = logging.getLogger(__name__)

class BaseCrudRepository(Generic[BaseDbModelType, BaseSchemaType], BaseCrudInterface[BaseSchemaType]):
    model: Type[BaseDbModelType] = NotImplemented  # SQLAlchemy модель
    schema: Type[BaseSchemaType] = NotImplemented  # Pydantic схема
    _FIELDS_TO_ALWAYS_EXCLUDE_FROM_CREATE_OR_UPDATE: set = set()

    def __init__(self, provider: SessionProviderInterface) -> None:
        self.session_provider = provider
        self._inspector = inspect(self.model)
        self.pk = {
            key.name: getattr(self.model, key.name)
            for key in self._inspector.primary_key
        }
        self.relations = {}
        self.joins = defaultdict(dict)
        self._add_unique = False
        self.aliases = {}
        self.fields = {
            column.key: getattr(self.model, column.key)
            for column in self._inspector.columns
        }
        self.table = self._inspector.tables[0].name
        for r in self._inspector.relationships.keys():
            # ищем поле с типом relation модели таблицы
            # заполним словарь outerjoin - поля для которых join(Х, isouter=True)
            # заполним словарь fields - поля модели (включая relation) для сортировки
            #
            relation = getattr(self.model, r)
            aliased_relation = aliased(relation.entity.class_)
            if hasattr(relation, "info") and relation.info.get("is_aliased", None):
                self.aliases[f"{relation}"] = aliased_relation
                self.joins[f"{relation}"]["onclause"] = [local_col == getattr(aliased_relation, remote_col.key) for local_col, remote_col in relation.prop.local_remote_pairs]
            self.relations[r] = aliased_relation
            self.joins[f"{relation}"]["isouter"] = not relation.property.innerjoin

            rel_mod_inspect = inspect(relation.entity.class_)
            for column in rel_mod_inspect.columns:
                self.fields[f"{r}.{column.key}"] = getattr(aliased_relation, column.key)

    def _prepare_options_for_model(
        self, schema: Type[BaseSchemaType], options: dict | None = None
    ) -> dict:
        """Формирует словарь с опциями для select операции. Используется
         для загрузки relation:
         ключ словаря - поле для join,
         значение - поля помеченное как contains_eager
         В опциях используем contains_eager, чтобы можно было загрузить
         relation c помощью join
        Args:
            options: словарь полученный на этапе формирования условий where
        Returns:
            dict опций
        """
        if not options:
            options = dict()
        for field in schema.model_fields.keys():
            if not hasattr(self.model, field):
                continue
            column = getattr(self.model, field)
            if column in options:
                continue
            if isinstance(column.property, RelationshipProperty):
                if f"{column}" in self.aliases:
                    options[column] = contains_eager(column, alias=self.aliases[f"{column}"])
                else:
                    options[column] = contains_eager(column)
        return options

    def _prepare_order(
        self,
        order: tuple[str, ...],
    ) -> list:
        """Формирует список сортировки для order_by()
        Args:
            order: список полей для сортировки
             по умолчанию выполняется asc сортировка,
             если имя поля начинается с "-", то desc сортировка
        Returns:
            список колонок сортировки
        """
        order_statements = []

        for field in order:
            direction = asc
            if field.startswith("-"):
                field = field[1:]
                direction = desc
            if "." not in field:
                field = f"{self.table}.{field}"
            order_statements.append(direction(text(field)))
        return order_statements

    def _process_join(self, statement: Select, options: dict) -> Select:
        for join_column in options.keys():
            if f"{join_column}" in self.aliases:
                statement = statement.join(
                    self.aliases[f"{join_column}"],
                    *self.joins[f"{join_column}"]["onclause"],
                    isouter=self.joins[f"{join_column}"]["isouter"]
                )
                self._add_unique = True
                continue
            statement = statement.join(
                join_column, isouter=self.joins[f"{join_column}"]["isouter"]
            )
        statement = statement.options(*list(options.values()))
        return statement

    # @autologger(logger)
    async def _filter_statement_prepare(
        self,
        schema: Type[BaseSchemaType]|Type[SchemaType],
        filters: dict,
        sa_filters: list,
        order: tuple[str, ...],
        limit: int,
        offset: int,
        session: AsyncSession,
        statement: Select | None = None,
        with_count: bool = False,
    ) -> (Select, int):
        """Формирует Select: подготавливает и применяет where, join, options, limit, offset.
        Так же, при необходимости, возвращает общее количество записей для сформированного
        запроса без учета offset, limit.
        Args:
            schema: схема Pydantic для формирования полей необходимых в ответе
            filters: словарь условий из которых формируется where ("field": value, "model.field": value)
            sa_filters: список условий для where, загружаемый непосредственно в where, без обработки
            order: набор полей для сортировки
            session: сессия доступа к БД
            statement: базовое выражение для формирования Select
            with_count: подсчитать общее количество записей для запроса без учета offset, limit
        Returns:
            Select, общее количество записей
        """
        statement = statement or select(self.model)
        where, options = prepare_where_clause(model=self.model, filters=filters, aliases=self.aliases)
        options = self._prepare_options_for_model(schema, options)
        if sa_filters:
            where.extend(sa_filters)
        statement = statement.where(*where)

        count = await get_record_count(session, statement) if with_count else -1
        if options:
            statement = self._process_join(statement, options)
        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)
        if order:
            statement = statement.order_by(*self._prepare_order(order))
        return statement, count

    @session_manager
    @autologger(logger)
    async def create(
        self,
        instance: BaseSchemaType | Sequence[BaseSchemaType],
        *,
        exclude_fields: set | None = None,
        with_relations: bool = False,
        session: AsyncSession = None,
    )->BaseSchemaType| Sequence[BaseSchemaType]:
        """Создает запись в БД из экземпляра схемы
        Args:
            instance: экземпляр схемы данных
            exclude_fields: поля, которые исключаются из model_dump
            with_relations: если передано - то создаем записи в БД для relations
            session: сессия доступа к БД
        Returns:
            экземпляр схемы данных
        """
        db_instances = []
        exclude_fields = exclude_fields or set()
        exclude_fields.update(self._FIELDS_TO_ALWAYS_EXCLUDE_FROM_CREATE_OR_UPDATE)
        if not isinstance(instance, Sequence):
            instances = [
                instance,
            ]
        else:
            instances = instance

        for instance in instances:
            if with_relations:
                for field, value in inspect(self.model).relationships.items():
                    if value.viewonly:
                        continue
                    subinstance = getattr(instance, field)
                    if not subinstance:
                        continue
                    db_instances.append(
                        instance_to_model(
                            instance=subinstance,
                            model=value.mapper.class_,
                            exclude_fields=exclude_fields,
                        )
                    )
            db_instances.append(
                instance_to_model(
                    instance=instance, model=self.model, exclude_fields=exclude_fields
                )
            )
        session.add_all(db_instances)
        # await session.flush()
        return instance

    async def _update(
        self,
        instance: BaseSchemaType | None = None,
        *,
        filters: dict | tuple[str, ...] | None = None,
        exclude_fields: tuple[str, ...] | None = None,
        update_fields: dict | tuple[str, ...] | None = None,
        exclude_none: bool = True,
        session: AsyncSession | None = None,
    ) -> BaseSchemaType:
        """Обновляет запись в БД из экземпляра схемы.
        Args:
            instance: экземпляр схемы данных
            filters: поля (значения берутся из instance) или условия для поиска (словарь, поле:значение), если
              не передано - используются primary key модели
            exclude_fields: поля, которые исключаются из model_dump
            update_fields: если передано tuple - то обновляем только эти поля, если передан dict,
             то используем его для обновления значений
            exclude_none: исключить при дампе схемы Pydantic оля со значением None.
              По умолчанию: True
            session: сессия доступа к БД
        Returns:
            экземпляр схемы данных
        """
        if not instance and not isinstance(update_fields, dict):
            raise ValueError(
                "if instance is none update_fields must be dict for update or vice versa"
            )
        if not filters:
            filters = {pk_f: getattr(instance, pk_f) for pk_f in self.pk.keys()}
        if isinstance(filters, tuple):
            if not instance:
                raise ValueError(f"{instance} is None")
            filters = {f: getattr(instance, f) for f in filters}

        update_data = (
            update_fields
            if isinstance(update_fields, dict)
            else prepare_update_data(
                instance=instance,
                model=self.model,
                exclude_fields=exclude_fields,
                update_fields=update_fields,
                exclude_none=exclude_none,
            )
        )

        results = await self._update_many(
            filters=filters,
            update_data=update_data,
            session=session,
        )
        if len(results) != 1:
            raise ValueError(f"update return not one object: {results}")
        return results[0]

    @session_manager
    @autologger(logger)
    async def update(
        self,
        instance: BaseSchemaType | None = None,
        *,
        filters: dict | tuple[str, ...] | None = None,
        exclude_fields: tuple[str, ...] | None = None,
        update_fields: dict | tuple[str, ...] | None = None,
        session: AsyncSession | None = None,
        exclude_none: bool = True,
    ) -> BaseSchemaType:
        """Обновляет запись в БД из экземпляра схемы.
        Args:
            instance: экземпляр схемы данных. Если в экземпляре присутствуют значения None,
              которые не должны попасть в БД, то нужно передать список полей в параметре
              update_fields
            filters: поля (значения берутся из instance) или условия для поиска (словарь, поле:значение),
              если не передано - используются primary key модели
            exclude_fields: поля, которые исключаются из model_dump
            update_fields: если передано tuple - то обновляем только эти поля, если передан dict,
             то используем его для обновления значений
            exclude_none: исключить при дампе схемы Pydantic поля со значением None.
              По умолчанию: True
            session: сессия доступа к БД
        Returns:
            экземпляр схемы данных
        """
        return await self._update(
            instance,
            filters=filters,
            exclude_fields=exclude_fields,
            update_fields=update_fields,
            exclude_none=exclude_none,
            session=session,
        )

    @session_manager
    @autologger(logger)
    async def update_many(
        self,
        *,
        update_data: dict,
        filters: dict,
        exclude_fields: tuple[str, ...] | None = None,
        session: AsyncSession | None = None,
    ) -> list[BaseSchemaType]:
        """Обновляет несколько строк в БД с использованием переданного словаря.
        Args:
            update_data: словарь полей и значений для обновления, для обновления
             отношений используются вложенные словари
            filters: поля (значения берутся из instance) или условия для поиска
             (словарь, поле:значение), если не передано - используются primary key модели
            exclude_fields: поля, которые исключаются из model_dump
            session: сессия доступа к БД
        Returns:
            экземпляр схемы данных
        """

        return await self._update_many(
            update_data=update_data, filters=filters, session=session
        )

    async def _update_many(
        self,
        *,
        update_data: dict,
        filters: dict,
        session: AsyncSession | None = None,
    ) -> list[BaseSchemaType]:
        """Обновляет несколько строк в БД с использованием переданного словаря.
        Args:
            update_data: словарь полей и значений для обновления, для обновления
             отношений используются вложенные словари
            filters: поля (значения берутся из instance) или условия для поиска
             (словарь, поле:значение), если не передано - используются primary key модели
            session: сессия доступа к БД
        Returns:
            экземпляр схемы данных
        """
        lookup_clause, options = prepare_where_clause(model=self.model, filters=filters, aliases=self.aliases)
        statement = select(self.model)

        options = self._prepare_options_for_model(schema=self.schema, options=options)
        statement = statement.where(*lookup_clause)
        if options:
            statement = self._process_join(statement, options)
        rows = (await session.execute(statement.with_for_update(of=self.model))).scalars()
        if self._add_unique:
            rows = rows.unique()

        results = update_rows(self.schema, rows.all(), update_data)
        return results

    @session_manager
    @autologger(logger)
    async def update_or_create(
        self,
        instance: BaseSchemaType,
        *,
        with_relations: bool = False,
        filters: dict | tuple[str, ...] | None = None,
        exclude_fields: tuple[str, ...] | None = None,
        update_fields: tuple[str, ...] | None = None,
        exclude_none: bool = True,
        session: AsyncSession | None = None,
    ) -> tuple[bool, BaseSchemaType]:
        """Обновляет или создает запись.
        Args:
            instance: экземпляр схемы данных
            with_relations: создать записи в БД для relation из instance
            filters: поля (значения берутся из instance) или условия для поиска (словарь, поле:значение), если
              не передано - используются primary key модели
            exclude_fields: поля, которые исключаются из model_dump
            update_fields: если передано - то обновляем только эти поля
            exclude_none: исключить при дампе схемы Pydantic поля со значением None.
              По умолчанию: True
            session: сессия доступа к БД
        Returns:
            is_created, экземпляр схемы данных
        """

        try:
            instance = await self._update(
                instance,
                filters=filters,
                exclude_fields=exclude_fields,
                update_fields=update_fields,
                exclude_none=exclude_none,
                session=session,
            )
            await session.flush()
            return False, instance
        except ValueError:
            await self.create(instance, with_relations=with_relations, session=session)
            return True, instance

    @session_manager
    @autologger(logger)
    async def delete(
        self, filters: dict, *, session: AsyncSession | None = None
    ) -> int:
        where, _ = prepare_where_clause(model=self.model, filters=filters)
        statement = delete(self.model).where(*where)
        result = await session.execute(statement)
        return result.rowcount

    @session_manager
    async def get_or_none(
        self,
        filters: dict,
        *,
        response_schema: Type[SchemaType] = None,
        order: tuple[str, ...] = None,
        session: AsyncSession | None = None,
    ) -> BaseSchemaType |SchemaType| None:
        result = await self.filter(
            filters=filters,
            session=session,
            response_schema=response_schema,
            order=order,
        )
        return result[0] if len(result) else None

    @session_manager
    async def get(
        self,
        filters: dict,
        *,
        response_schema: Type[SchemaType] = None,
        order: tuple[str, ...] = None,
        session: AsyncSession = None,
    ) -> BaseSchema|SchemaType:
        item = await self.get_or_none(
            response_schema=response_schema,
            filters=filters,
            session=session,
            order=order,
        )
        if not item:
            raise ValueError(f"Not found {self.model} for {filters}")
        return item

    @session_manager
    async def all(
        self,
        response_schema: Type[SchemaType] = None,
        order: tuple[str, ...] = None,
        session: AsyncSession | None = None,
    ) -> list[BaseSchemaType|SchemaType]:
        return await self.filter(
            filters={}, session=session, response_schema=response_schema, order=order
        )

    @session_manager
    async def filter_statement(
        self,
        statement: Select,
        *,
        response_schema: Type[SchemaType] = None,
        session: AsyncSession | None = None,
        is_use_scalars: bool = True,
    ) -> list[BaseSchemaType|SchemaType]:
        """Выбор из БД записей по фильтрам
        Args:
            statement: выражение select
            response_schema: схема в которую будут преобразованы данные из БД
            session: сессия доступа к БД
            is_use_scalars: выставляется в False при использовании в statement
             произвольных возвращаемых полей, а не SqlAlchemy модели
        Returns:
            список экземпляр схемы данных
        """
        schema = response_schema or self.schema
        query = await session.execute(statement)
        if is_use_scalars:
            query = query.scalars()
        if self._add_unique:
            query = query.unique()
        rows = query.all()
        return [schema.model_validate(row) for row in rows]

    @session_manager
    async def filter_statement_with_count(
        self,
        statement: Select,
        *,
        response_schema: Type[SchemaType] = None,
        limit: int | None = None,
        offset: int | None = None,
        session: AsyncSession | None = None,
        count_stmt: Select | None = None,
        is_use_scalars: bool = True,
    ) -> tuple[int, list[BaseSchemaType|SchemaType]]:
        """Выбор из БД записей по фильтрам
        Args:
            statement: выражение select
            response_schema: схема в которую будут преобразованы данные из БД
            limit: max количество возвращаемых записей
            offset: сдвиг от начала в БД
            session: сессия доступа к БД
            count_stmt: отдельный запрос для подсчета общего количества строк,
             может потребоваться в случае сложного запроса с group_by, order_by
            is_use_scalars: выставляется в False при использовании в statement
             произвольных возвращаемых полей, а не SqlAlchemy модели
        Returns:
            список экземпляр схемы данных
        """
        schema = response_schema or self.schema
        #
        # Для отдельных запросов которые используют group_by, order_by
        # необходимо правильно сформировать название полей, сделать это
        # динамически не представляется возможным, поэтому в таких случаях
        # передаем отдельное выражение для общего подсчета строк
        #
        #
        if count_stmt is None:
            count_stmt = statement.with_only_columns(*list(self.pk.values()))
            count_stmt = count_stmt.subquery()
        count = await get_record_count(session, count_stmt)

        if limit:
            statement = statement.limit(limit)
        if offset:
            statement = statement.offset(offset)

        query = await session.execute(statement)
        if is_use_scalars:
            query = query.scalars()
        rows = query.all()
        return count, [schema.model_validate(row) for row in rows]

    # @session_manager
    async def _filter(
        self,
        filters: dict,
        *,
        order: tuple[str, ...] = None,
        sa_filters: list = None,
        response_schema: Type[SchemaType] = None,
        session: AsyncSession | None = None,
        limit: int = 0,
        offset: int = 0,
        statement: Select | None = None,
    ) -> list[BaseSchemaType|SchemaType]:
        """Выбор из БД записей по фильтрам
        Args:
            filters: условия для поиска (словарь, поле:значение)
            order: список полей для упорядочивания
            sa_filters: список условий для where в формате sqlalchemy (не требует обработки)
            response_schema: схема в которую будут преобразованы данные из БД
            session: сессия доступа к БД
            limit: max количество возвращаемых записей
            offset: сдвиг от начала в БД
        Returns:
            список экземпляр схемы данных
        """
        schema = response_schema or self.schema
        statement, _ = await self._filter_statement_prepare(
            schema=schema,
            filters=filters,
            sa_filters=sa_filters,
            order=order,
            limit=limit,
            offset=offset,
            session=session,
            statement=statement,
        )

        return await self.filter_statement(
            statement, response_schema=schema, session=session
        )

    @session_manager
    @autologger(logger)
    async def filter(
        self,
        filters: dict,
        *,
        order: tuple[str, ...] = None,
        response_schema: Type[SchemaType] = None,
        session: AsyncSession | None = None,
        limit: int = 0,
        offset: int = 0,
        sa_filters: tuple = None,
    ) -> list[BaseSchemaType|SchemaType]:
        """Выбор из БД записей по фильтрам
        Args:
            filters: условия для поиска (словарь, поле:значение)
            order: список полей для упорядочивания
            response_schema: схема в которую будут преобразованы данные из БД
            session: сессия доступа к БД
            limit: max количество возвращаемых записей
            offset: сдвиг
            sa_filters: список условий для where в формате sqlalchemy (не требует обработки)
        Returns:
            список экземпляров схемы данных
        """
        return await self._filter(
            filters,
            order=order,
            response_schema=response_schema,
            session=session,
            limit=limit,
            offset=offset,
            sa_filters=sa_filters,
        )

    # @session_manager
    async def _filter_with_total_count(
        self,
        filters: dict,
        *,
        order: tuple[str, ...] = None,
        sa_filters: list = None,
        response_schema: Type[SchemaType] = None,
        session: AsyncSession | None = None,
        limit: int = 0,
        offset: int = 0,
        statement: Select | None = None,
    ) -> (int, list[BaseSchemaType|SchemaType]):
        """Выбор из БД записей по фильтрам, при этом будет дополнительно возвращено
         общее количество записей, соответствующее условиям поиска, без учета limit & offset
        Args:
            filters: условия для поиска (словарь, поле:значение)
            order: список полей для упорядочивания
            sa_filters: список условий для where в формате sqlalchemy (не требует обработки)
            response_schema: схема в которую будут преобразованы данные из БД
            session: сессия доступа к БД
            limit: max количество возвращаемых записей
            offset: сдвиг
        Returns:
            список экземпляров схемы данных
        """
        schema = response_schema or self.schema

        statement, count = await self._filter_statement_prepare(
            schema=schema,
            filters=filters,
            sa_filters=sa_filters,
            order=order,
            limit=limit,
            offset=offset,
            session=session,
            with_count=True,
            statement=statement,
        )

        return count, await self.filter_statement(
            statement, response_schema=schema, session=session
        )

    @session_manager
    async def filter_with_total_count(
        self,
        filters: dict,
        *,
        order: Sequence[str, ...] = None,
        response_schema: Type[SchemaType]= None,
        session: AsyncSession | None = None,
        limit: int = 0,
        offset: int = 0,
        sa_filters: Sequence = None,
    ) -> (int, list[BaseSchemaType|SchemaType]):
        """Выбор из БД записей по фильтрам, при этом будет дополнительно возвращено
         общее количество записей, соответствующее условиям поиска, без учета limit & offset
        Args:
            filters: условия для поиска (словарь, поле:значение)
            order: список полей для упорядочивания
            response_schema: схема в которую будут преобразованы данные из БД
            session: сессия доступа к БД
            limit: max количество возвращаемых записей
            offset: сдвиг
            sa_filters: список условий для where в формате sqlalchemy (не требует обработки)
        Returns:
            список экземпляр схемы данных
        """

        return await self._filter_with_total_count(
            filters,
            order=order,
            response_schema=response_schema,
            session=session,
            limit=limit,
            offset=offset,
            sa_filters=sa_filters,
        )
