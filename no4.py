from datetime import datetime

class Certificate:
    def __init__(self, no, date, fio, stipend, place):
        # Используем __setattr__ для установки значений
        self.no = no
        self.date = date
        self.fio = fio
        self.stipend = stipend
        self.place = place

    def __setattr__(self, key, value):
        # Валидация и контроль записи значений
        if key == 'no':
            if not isinstance(value, int) or value <= 0:
                raise ValueError("№ должен быть положительным целым числом")
        elif key == 'date':
            # Поддерживаем либо строку в формате YYYY-MM-DD, либо datetime
            if isinstance(value, str):
                try:
                    datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    raise ValueError("Дата должна быть в формате YYYY-MM-DD")
            elif not isinstance(value, datetime):
                raise ValueError("Дата должна быть строкой или datetime объектом")
        elif key == 'fio':
            if not isinstance(value, str) or not value.strip():
                raise ValueError("ФИО должно быть непустой строкой")
        elif key == 'stipend':
            if not (isinstance(value, (int, float)) and value >= 0):
                raise ValueError("Размер стипендии должен быть неотрицательным числом")
        elif key == 'place':
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Куда выдается справка должно быть непустой строкой")
        super().__setattr__(key, value)

    def __repr__(self):
        return (f"Certificate(№={self.no}, дата={self.date}, ФИО='{self.fio}', "
                f"стипендия={self.stipend}, куда='{self.place}')")

    def to_dict(self):
        # Для сохранения в CSV
        return {
            '№': self.no,
            'дата': self.date if isinstance(self.date, str) else self.date.strftime('%Y-%m-%d'),
            'ФИО студента': self.fio,
            'размер стипендии': self.stipend,
            'куда выдается справка': self.place
        }

# Наследование: расширенный класс с дополнительным методом
class ScholarshipCertificate(Certificate):
    def is_high_stipend(self, threshold=1500):
        """Проверяет, превышает ли стипендия порог."""
        return self.stipend > threshold

class CertificateCollection:
    def __init__(self):
        self._certificates = []

    def __iter__(self):
        """Итератор по справкам"""
        return iter(self._certificates)

    def __getitem__(self, index):
        """Доступ по индексу"""
        return self._certificates[index]

    def add(self, certificate):
        if not isinstance(certificate, Certificate):
            raise TypeError("Можно добавлять только объекты Certificate")
        self._certificates.append(certificate)

    def __repr__(self):
        return f"CertificateCollection({len(self._certificates)} certificates)"

    @staticmethod
    def from_csv(filename):
        import csv
        collection = CertificateCollection()
        with open(filename, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cert = ScholarshipCertificate(
                    no=int(row['№']),
                    date=row['дата'],
                    fio=row['ФИО студента'],
                    stipend=float(row['размер стипендии']),
                    place=row['куда выдается справка']
                )
                collection.add(cert)
        return collection

    def save_to_csv(self, filename):
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['№', 'дата', 'ФИО студента', 'размер стипендии', 'куда выдается справка']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for cert in self._certificates:
                writer.writerow(cert.to_dict())

    def sort_by_field(self, field, reverse=False):
        """Сортировка по полю (строковому или числовому)"""
        if not self._certificates:
            return
        if not hasattr(self._certificates[0], field):
            raise AttributeError(f"Поле '{field}' отсутствует в Certificate")
        self._certificates.sort(key=lambda c: getattr(c, field), reverse=reverse)

    def filter_by_stipend(self, min_value):
        """Генератор справок с стипендией больше min_value"""
        for cert in self._certificates:
            if cert.stipend > min_value:
                yield cert

    def __len__(self):
        return len(self._certificates)

# Пример использования
def main():
    filename = 'data.csv'

    # Загружаем коллекцию из файла
    collection = CertificateCollection.from_csv(filename)
    print("Загруженные справки:")
    for c in collection:
        print(c)

    # Сортировка по ФИО (строковое поле)
    collection.sort_by_field('fio')
    print("\nОтсортировано по ФИО:")
    for c in collection:
        print(c)

    # Сортировка по размеру стипендии (числовое поле)
    collection.sort_by_field('stipend', reverse=True)
    print("\nОтсортировано по размеру стипендии (по убыванию):")
    for c in collection:
        print(c)

    # Фильтрация с использованием генератора
    print("\nСтипендия больше 1500:")
    for c in collection.filter_by_stipend(1500):
        print(c)

    # Добавление новой записи
    print("\nДобавление новой справки:")
    new_cert = ScholarshipCertificate(
        no=len(collection) + 1,
        date='2025-06-19',
        fio='Сидоров Сидор Сидорович',
        stipend=1800,
        place='Банк'
    )
    collection.add(new_cert)
    print(new_cert)

    # Сохраняем обратно
    collection.save_to_csv(filename)
    print(f"\nДанные сохранены в файл {filename}")

if __name__ == '__main__':
    main()

'''
ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ 
ИЗМЕНЕНИЯ 
ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ 
ИЗМЕНЕНИЯ ИЗМЕНЕНИЯ 

'''