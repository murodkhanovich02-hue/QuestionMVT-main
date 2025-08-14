from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages

from .models import Question, Answer
from .forms import LoginForm


def home_page(request):
    return render(request, 'home.html')

def admin_page(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'registration/admin.html', context)
def login_page_view(request):
    """Foydalanuvchi login sahifasi"""
    form = LoginForm(request.POST or None)
    questions = Question.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return render(request, 'registration/admin.html', {'questions': questions})  # Admin sahifasi
                else:
                    return redirect('home_page')  # Oddiy foydalanuvchi sahifasi
            else:
                messages.error(request, "Login yoki parol noto‘g‘ri!")
        else:
            messages.error(request, "Formani to‘g‘ri to‘ldiring!")

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_page')
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Question, Answer


def add_question(request):
    """Savol va javoblarni qo‘shish (soddalashtirilgan usul)"""
    if request.method == 'POST':
        question_text = request.POST.get('text')
        level = request.POST.get('level')
        answers = [
            request.POST.get('answer1'),
            request.POST.get('answer2'),
            request.POST.get('answer3')
        ]
        correct_answer_index = request.POST.get('correct_answer')

        # Formani tekshirish
        if not question_text or not level or not all(answers) or not correct_answer_index:
            messages.error(request, "Iltimos, barcha maydonlarni to‘ldiring.")
            return render(request, 'question_add.html')

        try:
            with transaction.atomic():
                # Savol yaratish
                question = Question.objects.create(text=question_text, level=level)

                # Javoblarni yaratish
                created_answers = []
                for i, ans_text in enumerate(answers, start=1):
                    created_answers.append(
                        Answer.objects.create(
                            question=question,
                            text=ans_text,
                            is_correct=(str(i) == correct_answer_index)
                        )
                    )

                # To‘g‘ri javobni question modelida saqlash
                question.correct_answer = created_answers[int(correct_answer_index) - 1]
                question.save()

            messages.success(request, "✅ Savol muvaffaqiyatli qo‘shildi!")
            return render(request, 'question_add.html')

        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {e}")
            return render(request, 'question_add.html')

    return render(request, 'question_add.html')


def question_view(request):
    """Tanlangan level bo‘yicha test savollarini ko‘rsatish"""
    selected_level = request.GET.get('level', 'beginner')
    questions = Question.objects.filter(level=selected_level)
    return render(request, 'questions.html', {
        'questions': questions,
        'selected_level': selected_level
    })


def delete_question(request, question_id):
    """Savolni o‘chirish"""
    question = get_object_or_404(Question, id=question_id)
    questions = Question.objects.all()

    if request.method == "POST":  # Faqat POST orqali o‘chirilsin
        question.delete()
        messages.success(request, "✅ Savol muvaffaqiyatli o‘chirildi.")
        return render(request, 'registration/admin.html', {'questions': questions})  # Admin panel url nomini moslashtir

    return render(request, "confirm_delete.html", {"question": question})


def update_question(request, question_id):
    """Savolni yangilash"""
    question = get_object_or_404(Question, id=question_id)
    questions = Question.objects.all()

    if request.method == 'POST':
        text = request.POST.get('text')
        level = request.POST.get('level')

        if not text or not level:
            messages.error(request, "❌ Iltimos, barcha maydonlarni to‘ldiring.")
            return render(request, 'update_question.html', {'question': question})

        question.text = text
        question.level = level
        question.save()

        messages.success(request, "✅ Savol muvaffaqiyatli yangilandi!")
        return render(request, 'registration/admin.html', {'questions': questions})  # Admin panel URL nomini moslashtir

    return render(request, 'update_question.html', {'question': question})


def submit_answers(request):
    """Test natijasini hisoblash"""
    if request.method == 'POST':
        score = 0
        total = Question.objects.count()

        for question in Question.objects.all():
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1

        percentage = (score / total) * 100 if total > 0 else 0

        return render(request, 'results.html', {
            'score': score,
            'total': total,
            'percentage': round(percentage, 2)
        })

    return redirect('question_view')
