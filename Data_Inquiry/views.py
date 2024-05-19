from django.shortcuts import render
from Data_Crawling.models import CloserRanking

# 동적
from django.http import JsonResponse
from django.template.loader import render_to_string

# character_search 렌더링
def character_search(request):
    return render(request, 'character_search.html')

# ajax
def character_search_ajax(request):
    search_type = request.POST.get('search_type')
    search_query = request.POST.get('closer_name')

    closer_data = None
    if search_query:
        if search_type == 'character':
            temp_query = CloserRanking.objects.filter(character_name__iexact=search_query)
            extract_closer_name = temp_query.values_list('closer_name', flat=True).first()

            if extract_closer_name:
                closer_data = list(CloserRanking.objects.filter(
                    closer_name__iexact=extract_closer_name
                ).order_by('-total_combat_power_int'))

                temp_query_value = temp_query.first()
                closer_data = [item for item in closer_data if item != temp_query_value]
                closer_data.insert(0, temp_query_value)

        elif search_type == 'closer':
            closer_data = CloserRanking.objects.filter(closer_name__iexact=search_query).order_by('-total_combat_power_int')
    context = {
        'closer_data': closer_data,
        'search_query': search_query,
        'search_type': search_type,
    }
    html = render_to_string('includes/results.html', context)
    return JsonResponse({'html': html})