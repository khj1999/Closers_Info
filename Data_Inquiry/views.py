from django.shortcuts import render
from Data_Crawling.models import CloserRanking

# 동적
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# character_search 렌더링
def character_search(request):
    return render(request, 'character_search.html')

# character search ajax
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
    html = render_to_string('includes/user_results.html', context)
    return JsonResponse({'html': html})

# 랭킹 렌더링
def ranking_list(request):
    class_list = [
        '모든 캐릭터',
        '이세하',
        '이슬비',
        '서유리',
        '제이',
        '미스틸테인',
        '나타',
        '레비아',
        '하피',
        '티나',
        '바이올렛',
        '볼프강',
        '루나',
        '소마',
        '파이',
        '세트',
        '미래',
        '김철수',
        '은하',
        '루시',
        '애리',
    ]
    return render(request, 'ranking_list.html', {'class_list': class_list})

# 랭킹 ajax
# 랭킹 ajax
def ranking_list_ajax(request):
    if request.method == 'POST':
        character_type = request.POST.get('character_type')
        page = request.POST.get('page', 1)
        latest_date = CloserRanking.objects.aggregate(latest_date=Max('date'))['latest_date']
        
        if latest_date is None:
            return JsonResponse({'html': '<p>데이터가 없습니다.</p>'})
        
        if character_type == '모든 캐릭터':
            closer_data = CloserRanking.objects.filter(date=latest_date).order_by('-total_combat_power_int')
        else:
            closer_data = CloserRanking.objects.filter(date=latest_date, closer=character_type).order_by('-total_combat_power_int')
        
        paginator = Paginator(closer_data, 50)  # 한 페이지에 50명씩
        
        try:
            closer_data_page = paginator.page(page)
        except PageNotAnInteger:
            closer_data_page = paginator.page(1)
        except EmptyPage:
            closer_data_page = paginator.page(paginator.num_pages)
        
        # 페이지 범위 계산
        current_page = closer_data_page.number
        total_pages = paginator.num_pages
        start_page = max(current_page - 5, 1)
        end_page = min(current_page + 5, total_pages)
        page_range = range(start_page, end_page + 1)
        
        # 전체 순서 정보 추가
        start_index = (current_page - 1) * 50  # 현재 페이지 시작 인덱스 계산
        for index, item in enumerate(closer_data_page.object_list, start=start_index + 1):
            item.rank = index  # 각 객체에 순서 정보 추가

        context = {
            'character_type': character_type,
            'closer_data': closer_data_page,
            'page_range': page_range,
        }
        
        try:
            html = render_to_string('includes/ranking_results.html', context)
        except Exception as e:
            return JsonResponse({'html': f'<p>오류가 발생했습니다: {str(e)}</p>'})
        
        return JsonResponse({
            'html': html, 
            'has_next': closer_data_page.has_next(), 
            'has_previous': closer_data_page.has_previous(), 
            'page': closer_data_page.number, 
            'num_pages': paginator.num_pages
        })
    else:
        return JsonResponse({'html': '<p>잘못된 요청입니다.</p>'})
