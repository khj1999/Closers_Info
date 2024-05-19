from django.db import models

# Create your models here.
class CloserRanking(models.Model):
    date = models.DateField(verbose_name="날짜")
    ranking = models.CharField(max_length=50, verbose_name="랭킹")
    closer = models.CharField(max_length=50, verbose_name="클로저")
    closer_name = models.CharField(max_length=50, verbose_name="클로저명")
    level = models.CharField(max_length=50, verbose_name="레벨")
    grade = models.CharField(max_length=50, verbose_name="등급")
    character_name = models.CharField(max_length=50, verbose_name="캐릭터명")
    total_combat_power = models.CharField(max_length=50, verbose_name="종합 전투력")
    total_combat_power_int = models.IntegerField(verbose_name="종합 전투력(int)")

    def __str__(self):
        return f'클로저 명 : {self.closer_name}, 캐릭터 명 : {self.character_name} 클래스 명 : {self.closer}'