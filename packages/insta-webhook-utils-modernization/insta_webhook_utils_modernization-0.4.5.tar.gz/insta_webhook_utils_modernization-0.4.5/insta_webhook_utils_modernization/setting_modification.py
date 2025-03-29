import hashlib
import json
from typing import List, Dict, Any, Optional


def extract_required_fields(settings: List[Dict[str, Any]], required_fields: List[str]) -> List[Dict[str, Any]]:
    """Extract only the required fields from the settings."""
    extracted_settings = []

    for setting in settings:
        extracted = {field: setting.get(field) for field in required_fields}
        extracted_settings.append(extracted)

    return extracted_settings


def extract_required_fields_v2(settings: List[Dict[str, Any]], field_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
    """Extract fields based on the field mapping and return them in the new structure."""
    extracted_settings = []

    for setting in settings:
        extracted = {source_field: setting.get(target_field) for source_field, target_field in field_mapping.items()}
        extracted_settings.append(extracted)

    return extracted_settings


def build_single_key_lookup_table(
        settings: List[Dict[str, Any]],
        key_field: str
) -> Dict[Any, List[Dict[str, Any]]]:
    """Build a lookup table with a single key field."""

    lookup_table = {}

    for setting in settings:
        key_value = setting.get(key_field)

        if key_value is not None:
            if key_value in lookup_table:
                lookup_table[key_value].append(setting)
            else:
                lookup_table[key_value] = [setting]

    return lookup_table


def get_setting_by_single_key(
        lookup_table: Dict[Any, List[Dict[str, Any]]],
        key_value: Any
) -> Optional[List[Dict[str, Any]]]:
    """Fetch settings based on a single key in O(1) time."""
    return lookup_table.get(key_value, None)


def encode_in_sha256(input_string):
    """Generate a SHA256 hash of the given string."""
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()


async def get_parent_post_from_cached(category_ids, brand_ids, channel_type, social_id, redis_obj, logger):
    """Generate an SHA256 hash based on category ID, brand ID, channel type, and social ID."""
    try:
        # Build the base string using the provided parameters
        # Validate the social_id
        if not social_id:
            raise None
        category_list = category_ids.split(',')
        brand_list = brand_ids.split(',')
        data_to_send = []
        # Loop through both lists simultaneously
        for category_id, brand_id in zip(category_list, brand_list):
            base_string = f"{category_id}:{brand_id}:{channel_type}:"
            # Append the social_id to the base string
            base_string += social_id
            # Generate the SHA256 hash from the base string
            md5_cache_key = encode_in_sha256(base_string.lower())
            redis_data = redis_obj.get(f"sng:{md5_cache_key}")
            if redis_data:
                try:
                    data = json.loads(redis_data)
                    parent_data = {
                        "url": data.get("URL"),
                        "parent_post_social_id": data.get("SocialID"),
                        "is_parent_brand_post": data.get("IsBrandPost", False),
                        "comment_follower_count": data.get("UserInfo").get("FollowersCount", 0) or 0,
                        "comment_follows_count": data.get("UserInfo").get("FollowingCount", 0) or 0,
                        "comment_tweet_count": data.get("UserInfo").get("TweetCount", 0) or 0,
                    }
                    data_to_send.append(parent_data)
                except (ValueError, KeyError, json.decoder.JSONDecodeError) as ex:
                    logger.error(f"Error while fetching parent post data from redis: {ex}", exc_info=True)
                    continue
            else:
                logger.info(f"Cache miss for parent post data with key: sng:{md5_cache_key} and social_id: {social_id} brand_id: {brand_id} category_id: {category_id}")
        if data_to_send:
            return data_to_send
        return None
    except Exception as ex:
        logger.error(f"Error while creating the md5: {ex}", exc_info=True)
        return None


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(get_parent_post_from_cached('1861', '13011', '20', str(18145416208340297), None, None)))
