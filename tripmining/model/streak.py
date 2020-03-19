class Streak:
    """
    Captures checking streaks of the trip. Checking streaks are contiguous checkin sequences separated by given number
    of days of checking discontinuities
    """
    def __init__(self, first_date, last_date, days, days_gap):
        self.first_date = first_date
        self.last_date = last_date
        self.days = days
        self.inter_cluster_sparsity = self.__get_internal_cluster_penalty(days_gap)

    def __count_max_possible_unchecked_days(self, days_gap: int):
        total_count = 0
        current_date = self.first_date + 1
        current_count = 0
        while current_date < self.last_date:
            if current_count == days_gap - 1:
                current_count = 0
                current_date += 1
                continue
            else:
                current_count += 1
                current_date += 1
                total_count += 1
        return total_count

    def __get_internal_cluster_penalty(self, days_gap):
        number_of_unchecked_days = [day.number_of_checkins for day in self.days].count(0)
        count_max_possible_unchecked_days = self.__count_max_possible_unchecked_days(days_gap)
        if count_max_possible_unchecked_days == 0:
            return 0
        else:
            internal_steak_penalty = number_of_unchecked_days / count_max_possible_unchecked_days
            return internal_steak_penalty
