class AnalysisService:
    def sort_equipment_by_rate(self, equipment_list: list, ascending: bool = True) -> list:
        return sorted(equipment_list, key=lambda eq: eq.hourly_rate, reverse=not ascending)

    def sort_equipment_by_power(self, equipment_list: list, ascending: bool = True) -> list:
        return sorted(equipment_list, key=lambda eq: eq.power_rating, reverse=not ascending)

    def sort_rentals_by_duration(self, rental_list: list, ascending: bool = True) -> list:
        return sorted(rental_list, key=lambda r: r.get_rental_duration(), reverse=not ascending)

    def sort_rentals_by_client(self, rental_list: list, ascending: bool = True) -> list:
        return sorted(rental_list, key=lambda r: r.client_name, reverse=not ascending)

    def get_revenue_summary(self, rental_list: list, equipment_list: list) -> dict:
        total_fee = 0.0
        total_penalty = 0.0
        for r in rental_list:
            if r.status == "Returned":
                total_fee += r.calculate_rental_fee(equipment_list)
                if hasattr(r, 'calculate_late_penalty'):
                    total_penalty += r.calculate_late_penalty(equipment_list)
        return {
            "total_fee": total_fee,
            "total_penalty": total_penalty,
            "grand_total": total_fee + total_penalty
        }

    def get_top_rented_equipment(self, rental_list: list, equipment_list: list) -> list:
        from collections import defaultdict
        counts = defaultdict(int)
        for r in rental_list:
            for eq_id in r.equipment_ids:
                counts[eq_id] += 1
        
        eq_dict = {eq.equipment_id: eq for eq in equipment_list}
        top = [(eq_dict[eq_id], count) for eq_id, count in counts.items() if eq_id in eq_dict]
        top.sort(key=lambda x: x[1], reverse=True)
        return top
