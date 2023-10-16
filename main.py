from dataclasses import dataclass
import json
from typing import List


@dataclass
class Params:
    category_id: int


@dataclass
class CategoryRepositoryEntity:
    id: int
    name: str


@dataclass
class TagRepositoryEntity:
    id: int


@dataclass
class ProductRepositoryEntity:
    id: int
    name: str
    image: str


class CategoryRepository:
    def get_category_by_id(self, category_id: int) -> List[CategoryRepositoryEntity]:
        return [
            CategoryRepositoryEntity(id=1, name="Category 1"),
            CategoryRepositoryEntity(id=2, name="Category 2"),
        ]


class TagRepository:
    def get_tag_by_category_id(self, category_id: int) -> List[TagRepositoryEntity]:
        return [
            TagRepositoryEntity(id=1),
            TagRepositoryEntity(id=2),
        ]


class ProductRepository:
    def get_products_by_tag_id(self, tag_id: int) -> List[ProductRepositoryEntity]:
        return [
            ProductRepositoryEntity(id=1, name="Product 1", image="image_1.jpg"),
            ProductRepositoryEntity(id=2, name="Product 2", image="image_2.jpg"),
        ]


class CategoryException(Exception):
    pass


@dataclass
class ProductResultEntity:
    id: int
    name: str
    image: str


@dataclass
class TagsResultEntity:
    id: int
    products: list[ProductResultEntity]


@dataclass
class CategoryResultEntity:
    id: int
    name: str
    tags: list[TagsResultEntity]


class GetDomainPrefixHandler:
    def run(self) -> str:
        return "localhost"


class GetProductImageUrlHandler:
    def run(self, image: str) -> str:
        domain_prefix = GetDomainPrefixHandler().run()
        return f"htts://{domain_prefix}/media/{image}"


class GetCategoryDetailService:
    def run(self, params: Params):
        categories = CategoryRepository().get_category_by_id(params.category_id)

        if not categories:
            raise CategoryException

        category_result = []

        for category in categories:
            tags = TagRepository().get_tag_by_category_id(category.id)

            tags_result = []
            for tag in tags:
                products = ProductRepository().get_products_by_tag_id(tag.id)

                products_result = [
                    ProductResultEntity(
                        id=p.id,
                        name=p.name,
                        image=GetProductImageUrlHandler().run(p.image),
                    )
                    for p in products
                ]

                tags_result.append(
                    TagsResultEntity(
                        id=tag.id,
                        products=products_result,
                    )
                )

            category_result.append(
                CategoryResultEntity(
                    id=category.id, name=category.name, tags=tags_result
                )
            )

        return category_result


def respone_ok(value) -> None:
    data = json.dumps(value, default=lambda o: o.__dict__)
    print(data)


def respone_not_found() -> None:
    return None


def get_category_detail_view(request, category_id):
    params = Params(category_id=category_id)

    try:
        data = GetCategoryDetailService().run(params)
    except CategoryException:
        return respone_not_found()

    return respone_ok(data)


get_category_detail_view(request=None, category_id=1)


# [
#     {
#         "id": 1,
#         "name": "Category 1",
#         "tags": [
#             {
#                 "id": 1,
#                 "products": [
#                     {
#                         "id": 1,
#                         "name": "Product 1",
#                         "image": "htts://localhost/media/image_1.jpg",
#                     },
#                     {
#                         "id": 2,
#                         "name": "Product 2",
#                         "image": "htts://localhost/media/image_2.jpg",
#                     },
#                 ],
#             },
#             {
#                 "id": 2,
#                 "products": [
#                     {
#                         "id": 1,
#                         "name": "Product 1",
#                         "image": "htts://localhost/media/image_1.jpg",
#                     },
#                     {
#                         "id": 2,
#                         "name": "Product 2",
#                         "image": "htts://localhost/media/image_2.jpg",
#                     },
#                 ],
#             },
#         ],
#     },
#     {
#         "id": 2,
#         "name": "Category 2",
#         "tags": [
#             {
#                 "id": 1,
#                 "products": [
#                     {
#                         "id": 1,
#                         "name": "Product 1",
#                         "image": "htts://localhost/media/image_1.jpg",
#                     },
#                     {
#                         "id": 2,
#                         "name": "Product 2",
#                         "image": "htts://localhost/media/image_2.jpg",
#                     },
#                 ],
#             },
#             {
#                 "id": 2,
#                 "products": [
#                     {
#                         "id": 1,
#                         "name": "Product 1",
#                         "image": "htts://localhost/media/image_1.jpg",
#                     },
#                     {
#                         "id": 2,
#                         "name": "Product 2",
#                         "image": "htts://localhost/media/image_2.jpg",
#                     },
#                 ],
#             },
#         ],
#     },
# ]
