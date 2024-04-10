from django.conf.urls.static import static
from django.urls import path

from BudgetForecaster import settings
from budgets import views

app_name = "budgets"
urlpatterns = [
                  path('', views.user_login, name='login'),
                  path('home/<str:budget_set>', views.index, name='home'),
                  path('update/assumptions/', views.budget_assumptions, name='assumptions'),
                  path('create', views.create_user, name='create'),
                  path('report/', views.generate_excel, name='report'),
                  path('settings/', views.budget_settings, name='settings'),
                  path('settings/<int:dept_id>/', views.department_budget_settings, name='department-settings'),
                  path('logout/', views.user_logout, name='logout'),
                  path('assumptions/delete/<int:id>/', views.delete_assumption, name='delete-assumption'),
                  path('currency/delete/<int:id>/', views.delete_currency, name='delete-currency'),
                  path('update/expenses/<int:department_id>', views.update_expenses, name='update-expenses'),
                  path('delete_line/<int:object_id>/', views.clear_budget_line, name='clear-line'),
                  path('delete_budget/<int:id>/', views.clear_budget_line, name='clear-budget'),
                  path('update/<int:object_id>', views.update, name='update'),
                  path('update/field_comment/', views.saveComments, name='update-comment'),
                  path('update/expenses/account/search', views.accounts_search),
                  path('home/<str:budget_set>/opex/', views.opex_index, name='home-opex'),
                  path('home/dept/<str:budget_set>/', views.dept_user_index, name='home-dept'),
                  path('log/', views.changelog, name='changelog'),
                  path('enter-otp/', views.verify_otp, name='enter-otp'),
                  path('set_active/<int:id>/', views.toggle_status_true, name='set-active'),
                  path('set_inactive/<int:id>/', views.toggle_status_false,
                       name='set-inactive'),
                  path('set_incomplete/<int:id>/', views.toggle_status_incomplete,
                       name='set-incomplete'),
                  path('set_complete/<int:id>/', views.toggle_status_complete,
                       name='set-complete'),
                  path('post/<str:budget_set>/', views.post_to_sage, name='post-to-sage')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
