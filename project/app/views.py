from django.shortcuts import render
# from .Agent import get_sql_query, return_sql_response
from app.Agent import get_sql_query, return_sql_response
# Create your views here.


def home(request):
    retrieved_data = ''
    columns = []

    if request.method == 'POST':
        user_query = request.POST['user_query']
        sql_query = get_sql_query(user_query)  # Convert user query to SQL
        # retrieved_data = return_sql_response(sql_query)
        columns, retrieved_data = return_sql_response(sql_query)  # Execute SQL and get data

    return render(request, 'home.html', {'retrieved_data': retrieved_data, 'columns': columns})