from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def admin_only(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:

            return view_func(request,
                             *args,
                             **kwargs)

        return HttpResponse(
            "Access Denied"
        )

    return wrapper

@login_required
def home(request):

    total_books = Book.objects.count()
    total_members = Member.objects.count()
    issued_books = IssueBook.objects.filter(returned=False).count()

    context = {
        'total_books': total_books,
        'total_members': total_members,
        'issued_books': issued_books,
    }

    return render(request, 'home.html', context)


@login_required
@admin_only
def add_book(request):

    if request.method == 'POST':

        title = request.POST['title']
        author = request.POST['author']
        category = request.POST['category']
        quantity = request.POST['quantity']

        Book.objects.create(
            title=title,
            author=author,
            category=category,
            quantity=quantity,
            available=quantity
        )

        return redirect('books')

    return render(request, 'add_book.html')

@login_required
@admin_only
def edit_book(request, id):

    book = Book.objects.get(id=id)

    if request.method == 'POST':

        book.title = request.POST['title']
        book.author = request.POST['author']
        book.category = request.POST['category']

        quantity = int(request.POST['quantity'])

        book.quantity = quantity
        book.available = quantity

        book.save()

        return redirect('books')

    return render(request,
                  'edit_book.html',
                  {'book': book})

@login_required
@admin_only
def delete_book(request, id):

    book = Book.objects.get(id=id)

    book.delete()

    return redirect('books')

@login_required
@admin_only
def members(request):

    members = Member.objects.all()

    return render(request,
                  'members.html',
                  {'members': members})

@login_required
@admin_only
def add_member(request):

    memberships = Membership.objects.all()

    error = ""

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        membership_id = request.POST['membership']

        # Check if username already exists
        if User.objects.filter(username=username).exists():

            error = "Username already exists"

        else:

            user = User.objects.create_user(
                username=username,
                password=password
            )

            membership = Membership.objects.get(id=membership_id)

            Member.objects.create(
                user=user,
                phone=phone,
                membership=membership
            )

            return redirect('members')

    return render(request,
                  'add_member.html',
                  {
                      'memberships': memberships,
                      'error': error
                  })

@login_required
def issues(request):

    issues = IssueBook.objects.all()

    return render(request,
                  'issues.html',
                  {'issues': issues})

@login_required
def issue_book(request):

    members = Member.objects.all()
    books = Book.objects.filter(available__gt=0)

    error = ""

    if request.method == 'POST':

        member_id = request.POST['member']
        book_id = request.POST['book']
        return_date = request.POST['return_date']

        member = Member.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)

        if book.available <= 0:

            error = "Book not available"

        else:

            IssueBook.objects.create(
                member=member,
                book=book,
                issue_date=now().date(),
                return_date=return_date
            )

            # Reduce available books
            book.available -= 1
            book.save()

            return redirect('issues')

    return render(request,
                  'issue_book.html',
                  {
                      'members': members,
                      'books': books,
                      'error': error
                  })

@login_required
def return_book(request):

    issues = IssueBook.objects.filter(returned=False)

    today = date.today()

    for issue in issues:

        if today > issue.return_date:

            late_days = (today - issue.return_date).days

            issue.fine = late_days * 10

            issue.save()

    return render(request,
                  'return_book.html',
                  {'issues': issues})

@login_required
def return_book_confirm(request, id):

    issue = IssueBook.objects.get(id=id)

    # Prevent return if fine unpaid
    if issue.fine > 0 and not issue.fine_paid:

        return HttpResponse(
            "Please pay fine first"
        )

    issue.returned = True

    issue.save()

    # Increase available quantity
    book = issue.book

    book.available += 1

    book.save()

    return redirect('return_book')

@login_required
def pay_fine(request, id):

    issue = IssueBook.objects.get(id=id)

    issue.fine_paid = True

    issue.save()

    return redirect('return_book')

def user_login(request):

    error = ""

    if request.method == 'POST':

        role = request.POST['role']
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ADMIN LOGIN
            if role == "admin" and user.is_superuser:

                login(request, user)

                return redirect('home')

            # USER LOGIN
            elif role == "user" and not user.is_superuser:

                login(request, user)

                return redirect('home')

            else:

                error = "Invalid Role Selection"

        else:

            error = "Invalid Username or Password"

    return render(request,
                  'login.html',
                  {'error': error})

def user_logout(request):

    logout(request)

    return redirect('login')

@login_required
@admin_only
def reports(request):

    return render(request, 'reports.html')

@login_required
def available_books(request):

    books = Book.objects.filter(available__gt=0)

    return render(request,
                  'available_books.html',
                  {'books': books})


@login_required
def overdue_books(request):

    issues = IssueBook.objects.filter(
        returned=False,
        fine__gt=0
    )

    return render(request,
                  'overdue_books.html',
                  {'issues': issues})

@login_required
def master_books(request):

    books = Book.objects.all()

    return render(request,
                  'master_books.html',
                  {'books': books})

@login_required
def master_memberships(request):

    members = Member.objects.all()

    return render(request,
                  'master_memberships.html',
                  {'members': members})

@login_required
@admin_only
def manage_books(request):

    books = Book.objects.all()

    return render(request,
                  'manage_books.html',
                  {'books': books})

@login_required
def books(request):

    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    return render(request,
                  'books.html',
                  {'books': books})