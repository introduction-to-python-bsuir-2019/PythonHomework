# FinalTask

## 1 iter

Выполнена

## 2 iter

Выполнена

## 3 iter

Выполнена. 
Для хранения данных использовал pickle. Данные храню 
в папке Cache. Название файлов соответствуют дате статей, хранящихся там.
Отвечает за загрузку и выгрузку статей из файла класс Saver

## 4 iter

Выполнена
Данные сохраняю в формат html и pdf
В условиях не было указано в каком формате поставляется, поэтому выбрал для этого свой.
Путь должен содержать название файла и формат.
Примеры:
/home/ilya/snap/test.pdf
./test.html

## Help
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit LIMIT]
                  [--date DATE] [--to_html TO_HTML] [--to_pdf TO_PDF]
                  source
