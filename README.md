# News_Portal
Новостной портал, создаваемый с помощью django

Главное приложение - news. Для него созданы модели Author, Post, Comment и др.
Между моделями реализованы все типы связей, созданы методы для формирования рейтинга объектов и вывода информации об объекте.

Реализованы .views (news/views) и .templates (News_Portal/templates) для вывода всех статей на одной странице(/posts/), и вывода статьи по одной (/posts/1) 

Добавлена фильтрация для постов (/posts/) по категории, времени выхода поста и по ключевому слову

Добавлена кнопки для просмотра, редактирования и удаления постов. Вьюшки сделаны отдельно для двух типов постов: статьи и новости

Для создания новостей добавлена проверка прав пользователя. Если пользователь - администратор, он имеет права на добавление, удаление и редактирование новостей, если нет, то выходит ошибка 403.

Добавлена страница accounts/login для входа на портал
