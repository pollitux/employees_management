import pandas as pd


class PandasService:
    """
    Pandas service for the Employee Management UI.
    """

    @staticmethod
    def employees_to_dataframe(employees):
        """
        Generates a Pandas DataFrame inside a QTableWidget.
        :param employees:
        :return:
        """
        data = []
        for e in employees:
            data.append({
                "nss": e.nss,
                "first_name": e.first_name,
                "last_name_f": e.last_name_f,
                "last_name_m": e.last_name_m,
                "position": e.position_rel.name if e.position_rel else None,
                "municipality": e.municipality_rel.name if e.municipality_rel else None,
                "employee_type": e.employee_type,
                "hourly_rate": e.hourly_rate,
                "hours_worked": e.hours_worked,
                "birth_date": e.birth_date
            })

        df = pd.DataFrame(data)

        # Convert birth_date to datetime safely
        df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")

        # Calculate age correctly
        today = pd.Timestamp.today()
        df["age"] = (today - df["birth_date"]).dt.days // 365

        return df
