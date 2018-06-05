# GSEA_last_hw
last python homework

## Описание
Интерфейс для подсчета p-value теста Колмогорова-Смирнова 

## Запуск  
usage: gsea2_Skalon.py [-h] -i Str  
optional arguments:  
  -h, --help           show this help message and exit  
  -i Str, --input Str  Input file  

пример:python3 gsea2_Skalon.py -i ./gsea1/mainwindow.ui  

## Интерфейс
Программа выглядит так:  
![int](https://github.com/LisaSkalon/GSEA_last_hw/blob/master/mainwindow.png)

В окошко "номер файла" необходимо ввести название требуемого файла из базы данных GEO (без кавычек), в окошко "имена генов" - названия желаемых генов без кавычек и через пробел. Затем необходимо нажать кнопку "получить p-value".

