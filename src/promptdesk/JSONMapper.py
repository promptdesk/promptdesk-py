class JSONMapper:
    def __init__(self):
        pass
    
    def is_integer(self, s):
        if s.startswith('-'):
            return s[1:].isdigit()
        return s.isdigit()
        
    def get_from_dict(self, data_dict, map_path, default):
        if map_path is None:
            return default
        keys = map_path.split('.')
        collected_values = []
        def recurse(data, keys):
            if not keys:
                return data
            key = keys[0]
            if key == "*":
                if not isinstance(data, (list, tuple)):
                    return default
                for item in data:
                    result = recurse(item, keys[1:])
                    if result is not None:
                        collected_values.extend(result if isinstance(result, list) else [result])
            elif self.is_integer(key):
                key = int(key)
                if isinstance(data, (list, tuple)) and len(data) > key:
                    return recurse(data[key], keys[1:])
                else:
                    return default
            else:
                if isinstance(data, dict) and key in data:
                    return recurse(data[key], keys[1:])
                else:
                    return default
            return collected_values

        result = recurse(data_dict, keys)
        return result if collected_values else result

    def set_in_dict(self, data_dict, map_path, value, append_to=False, prepend_to=False):
        keys = map_path.split('.')
        for i, key in enumerate(keys[:-1]):
            if self.is_integer(key):
                key = int(key)
                while key >= len(data_dict):
                    data_dict.append({})
                data_dict = data_dict[key]
            else:
                if i < len(keys) - 2 and keys[i + 1].isdigit():  # Next key is a digit, ensure a list
                    data_dict = data_dict.setdefault(key, [])
                else:
                    data_dict = data_dict.setdefault(key, {})
        if append_to or prepend_to:
            # Ensure the target is a list
            if keys[-1] not in data_dict or not isinstance(data_dict[keys[-1]], list):
                data_dict[keys[-1]] = []
            if append_to:
                data_dict[keys[-1]].append(value)
            elif prepend_to:
                data_dict[keys[-1]].insert(0, value)
        else:
            # Handle the last key for direct set
            if self.is_integer(keys[-1]):
                last_key = int(keys[-1])
                while last_key >= len(data_dict):
                    data_dict.append(None)
                data_dict[last_key] = value
            else:
                data_dict[keys[-1]] = value

    def transform_value(self, value, transformation_rules):
        for condition in transformation_rules.get("conditions", []):
            if condition["when"]["field"] == "value":
                if value == condition["when"]["equals"]:
                    return condition["transformTo"]
            
        #keep for last
        for condition in transformation_rules.get("text", []):
            if condition == "uppercase":
                return value.upper()
            elif condition == "lowercase":
                return value.lower()
            elif condition == "strip":
                return value.strip()  
        return value  # Return original value if no conditions met

    def apply_subrules(self, source_item, subrules):
        temp_object = {}
        for subrule in subrules:
            source_value = self.get_from_dict(source_item, subrule['sourceField'], subrule.get('default', None))
            if source_value is None:
                source_value = subrule.get('default')
            # Check for transformation rule
            if "transformation" in subrule:
                source_value = self.transform_value(source_value, subrule["transformation"])
            self.set_in_dict(temp_object, subrule['targetField'], source_value, append_to=subrule.get('appendTo', False), prepend_to=subrule.get('prependTo', False))
        return temp_object

    def check_conditions(self, conditions, source_json, rule):
        for condition in conditions:
            source_value = self.get_from_dict(source_json, condition['sourceField'], None)
            if condition['check'] == 'equals':
                return source_value == condition['value']
            elif condition['check'] == 'not-equals':
                return source_value != condition['value']
            elif condition['check'] == 'exists':
                return source_value is not None
            else:
                raise ValueError(f"Unsupported check: {rule['check']}")
        
    def apply_mapping(self, source_json, mapping_rules):
        target_json = {}
        temp_storage = {}

        # Process rules to either directly set values or prepare them for grouped appending
        for rule in mapping_rules:
            #Process non-array mappings as before
            source_value = self.get_from_dict(source_json, rule['sourceField'], rule.get('default', None))
            if "conditions" in rule:
                is_condition_met = self.check_conditions(rule["conditions"], source_json, rule)
                if not is_condition_met:
                    continue
            if rule.get('action') == 'mapArray' and 'subRules' in rule:
                # Handle nested array mapping
                source_array = self.get_from_dict(source_json, rule['sourceField'], rule.get('default', None))
                if isinstance(source_array, list):
                    mapped_array = [self.apply_subrules(item, rule['subRules']) for item in source_array]
                    self.set_in_dict(target_json, rule['targetField'], mapped_array, append_to=rule.get('appendTo', False), prepend_to=rule.get('prependTo', False))
            else:
                if "transformation" in rule:
                    source_value = self.transform_value(source_value, rule["transformation"])
                if 'groupId' in rule:
                    if rule['groupId'] not in temp_storage:
                        temp_storage[rule['groupId']] = {}
                    temp_storage[rule['groupId']][rule['targetField']] = source_value
                else:
                    if 'targetField' not in rule:
                        return source_value
                    self.set_in_dict(target_json, rule['targetField'], source_value, append_to=rule.get('appendTo', False))

        # Append/prepend grouped items from temporary storage to the target structure
        for group_id, data in temp_storage.items():
            append_target = None
            prepend_target = None
            for rule in mapping_rules:
                if rule.get('groupId') == group_id:
                    if 'appendTo' in rule:
                        append_target = rule['appendTo']
                    elif 'prependTo' in rule:
                        prepend_target = rule['prependTo']
                    break
            if append_target:
                self.set_in_dict(target_json, append_target, data, append_to=True)
            elif prepend_target:
                self.set_in_dict(target_json, prepend_target, data, prepend_to=True)

        return target_json