class Scopes():
    @classmethod
    def summary_scope(self) -> int:
        return sum(set(self.scope_fields_db.keys())) + sum(set(self.scope_methods.values()))
    

    # Not implemented.
    scope_fields_db: dict[int, dict[str, type]] = {
        16: {'registration_date': int},
        32: {'banned': bool},
        64: {'role_name': str}
    }


    scope_methods: dict[str, int] = {
        'user_get': 0,
        'users_get': 0,
        'user_update': 1,
        }
    
