from django.conf.urls.static import static
from django.urls import path

from BudgetForecaster import settings
from budgets import views

app_name = "budgets"
urlpatterns = [
                  path('', views.user_login, name='login'),
                  path('home/', views.q1_values, name='dashboard-home'),
                  path('home/capex/', views.capex_index, name='home'),
                  path('update/assumptions/', views.budget_assumptions, name='assumptions'),
                  path('create', views.create_user, name='create'),
                  path('report/opex/', views.generate_excel_opex, name='report'),
                  path('report/capex/', views.generate_excel_capex, name='report-capex'),
                  path('reports/', views.reports, name='reports'),
                  path('pending/<str:department>/', views.pending_dashboard, name='pending'),
                  path('actual/<str:department>/', views.actual_dashboard, name='actual-dashboard'),
                  path('dashboard/content/', views.quarter_dashboard_index_department_table),
                  path('dashboard/content/search/', views.search_dashboard),
                  path('dashboard/content/search/results/<str:acct>/', views.search_results_dashboard, name='dashboard-search-results'),
                  path('home/department/', views.dashboard_index_department,name='dashboard-home-department'),
                  path('settings/', views.budget_settings, name='settings'),
                  path('settings/<int:dept_id>/', views.department_budget_settings, name='department-settings'),
                  path('logout/', views.user_logout, name='logout'),
                  path('assumptions/delete/<int:id>/', views.delete_assumption, name='delete-assumption'),
                  path('currency/delete/<int:id>/', views.delete_currency, name='delete-currency'),
                  path('update/expenses/<int:department_id>', views.update_expenses, name='update-expenses'),
                  path('delete_line/<int:object_id>/', views.clear_budget_line, name='clear-line'),
                  path('edit_line/<int:object_id>/', views.edit_line, name='edit-line'),
                  path('delete_budget/<int:object_id>/', views.clear_budget_numbers, name='clear-budget'),
                  path('update/<int:object_id>', views.update, name='update'),
                  path('update/field_comment/', views.saveComments, name='update-comment'),
                  path('account/search', views.accounts_search),
                  path('home/opex/', views.opex_index, name='home-opex'),
                  path('home/dept/', views.dept_user_index, name='home-dept'),
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
