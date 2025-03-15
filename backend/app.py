from flask import Flask, render_template, request
import scraping
import databasecode

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET', 'POST'])
def index():
  message = ''
  universities = None

  if request.method == 'POST' and 'start_parsing' in request.form:
    try:
      parsed_data = scraping.scrape_universities()
      new_data_count = 0

      for name, url, qs in parsed_data:
        new_data_count += databasecode.save_data(name, url, qs)

      record_count = databasecode.get_record_count()
      message = f"Парсинг успешен. Добавлено {new_data_count} новых уникальных записей. Всего записей: {record_count}"

    except Exception as e:
      message = f"Ошибка! Перезагрузите. Информация об ошибке: {e}"

  elif request.method == 'POST' and 'command' in request.form:
    command = request.form['command']

    if command == 'help':
      message = """
        Список команд:
        help - показать этот список.
        getall - получить все данные из базы данных.
        clearall - удалить все данные из базы данных.
        sortqs - cортировать по кол-ву доп программ образования.
      """

    elif command == 'getall':
      universities, record_count = databasecode.get_universities_with_ranks()
      message = f"Найдено {record_count} университетов."

    elif command == 'clearall':
      try:
        record_count = databasecode.get_record_count()
        databasecode.clear_all_data()
        message = f"Очищены все {record_count} записей"
      except Exception as e:
        message = f"Ошибка при удалении: {e}"

    elif command == 'sortqs':
      try:
        universities, record_count = databasecode.get_universities_with_ranks()
        universities = sorted(universities, key=lambda x: x[2] if x[2] is not None else float('-inf'), reverse=True)
        message = "Университеты отсортированы по доп программам."
      except Exception as e:
        message = f"Ошибка при сортировке: {e}"

    else:
      message = "Неизвестная команда"

  else:
    universities, record_count = databasecode.get_universities_with_ranks()

  return render_template('index.html', message=message, universities=universities)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
