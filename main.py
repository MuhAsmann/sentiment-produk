from urllib.parse import urlparse
import requests

GRAPHQL_URL = "https://gql.tokopedia.com/graphql"

headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
    "Content-Type": "application/json",
    "Origin": "https://www.tokopedia.com",
    "Referer": "https://www.tokopedia.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "x-source": "tokopedia-lite",
    "x-tkpd-lite-service": "zeus",
    "x-version": "1.0",
    "x-device": "desktop"
}

session = requests.Session()
session.headers.update(headers)

def parse_tokopedia_url(url: str):
    path = urlparse(url).path.strip("/")
    shop, product_key = path.split("/", 1)
    return shop, product_key


def safe_get(obj, *keys):
    """safe nested dict getter"""
    for k in keys:
        if obj is None:
            return None
        obj = obj.get(k)
    return obj


def get_product_info(shop, product_key):

    payload = [{
        "operationName": "PDPMainInfo",
        "variables": {
            "productKey": product_key,
            "shopDomain": shop,
            "layoutID": "",
            "extraPayload": "",
            "queryParam": "",
            "source": "P1",
            "userLocation": {
                "addressID": "",
                "districtID": "2274",
                "postalCode": "",
                "latlon": "",
                "cityID": "176"
            }
        },
        "query": """query PDPMainInfo(
            $productKey: String,
            $shopDomain: String,
            $layoutID: String,
            $extraPayload: String,
            $queryParam: String,
            $source: String,
            $userLocation: pdpUserLocation
        ) {
            pdpMainInfo(
                shopDomain: $shopDomain
                productKey: $productKey
                layoutID: $layoutID
                extraPayload: $extraPayload
                queryParam: $queryParam
                source: $source
                userLocation: $userLocation
            ) {
                data {
                    basicInfo {
                        alias
                        shopName
                        productID
                        stats {
                            rating
                            countReview
                        }
                    }
                }
            }
        }"""
    }]

    url = GRAPHQL_URL + "/PDPMainInfo"
    r = session.post(url, json=payload)
    print(url, payload)

    try:
        data = r.json()
    except:
        print("Invalid JSON response")
        print(r.text)
        return None

    basic = safe_get(data[0], "data", "pdpMainInfo", "data", "basicInfo")

    if not basic:
        print("Failed to get product info")
        print(data)
        return None

    return {
        "productID": basic.get("productID"),
        "shopName": basic.get("shopName"),
        "productName": basic.get("alias"),
        "rating": safe_get(basic, "stats", "rating"),
        "reviewCount": safe_get(basic, "stats", "countReview")
    }


def get_reviews(product_id, page=1, limit=50):

    payload = [{
        "operationName": "productReviewList",
        "variables": {
            "productID": product_id,
            "page": page,
            "limit": limit,
            "sortBy": "informative_score desc",
            "filterBy": ""
        },
        "query": """
        query productReviewList($productID: String!, $page: Int, $limit: Int, $sortBy: String, $filterBy: String) {
          productReviewList(productID: $productID, page: $page, limit: $limit, sortBy: $sortBy, filterBy: $filterBy) {
            list {
              id
              rating
              comment
              userName
              reviewDate
            }
          }
        }
        """
    }]

    url = GRAPHQL_URL + "/productReviewList"
    r = session.post(url, json=payload)

    try:
        data = r.json()
        return data[0]["data"]["productReviewList"]["list"]
    except:
        return []


def scrape_all_reviews(product_id):

    page = 1
    all_reviews = []

    while True:

        reviews = get_reviews(product_id, page)

        if not reviews:
            break

        all_reviews.extend(reviews)

        print(f"page {page} -> {len(reviews)} reviews")

        page += 1

    return all_reviews


def main():

    url = "https://www.tokopedia.com/butikgames/nintendo-switch-oled-cfw-128gb-256gb-512gb-full-game-1730699065287608236"

    shop, product_key = parse_tokopedia_url(url)

    print("shop:", shop)
    print("productKey:", product_key)

    product_info = get_product_info(shop, product_key)

    if not product_info:
        print("Failed to fetch product info")
        return

    print("product info:", product_info)

    product_id = product_info["productID"]

    reviews = scrape_all_reviews(product_id)

    print("total reviews:", len(reviews))


if __name__ == "__main__":
    main()