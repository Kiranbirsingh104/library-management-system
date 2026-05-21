from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('books/', views.books, name='books'),

    path('add-book/', views.add_book, name='add_book'),

    path('edit-book/<int:id>',
         views.edit_book,
         name='edit_book'),

    path('delete-book/<int:id>',
         views.delete_book,
         name='delete_book'),
    
    path('members/',
         views.members,
         name='members'),

    path('add-member/',
         views.add_member,
         name='add_member'),

    path('issues/',
         views.issues,
         name='issues'),

    path('issue-book/',
         views.issue_book,
         name='issue_book'),
    
    path('return-book/',
         views.return_book,
         name='return_book'),

    path('return-book-confirm/<int:id>',
         views.return_book_confirm,
         name='return_book_confirm'),

    path('login/',
         views.user_login,
         name='login'),

    path('logout/',
         views.user_logout,
         name='logout'),
         
    path('reports/',
         views.reports,
         name='reports'),

    path('available-books/',
         views.available_books,
         name='available_books'),

    path('overdue-books/',
         views.overdue_books,
         name='overdue_books'),
    
    path('pay-fine/<int:id>',
         views.pay_fine,
         name='pay_fine'),
    
    path('master-books/',
         views.master_books,
         name='master_books'),

    path('master-memberships/',
         views.master_memberships,
         name='master_memberships'),

    path('manage-books/',
         views.manage_books,
         name='manage_books'),
    

]