
import requests
from urllib.parse import urlparse
import time
import random

def get_headers():
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "content-type": "application/json",
        "origin": "https://www.tokopedia.com",
        "referer": "https://www.tokopedia.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-source": "tokopedia-lite",
        "x-tkpd-lite-service": "zeus",
        "x-version": "97a23db",
        "x-device": "desktop",
        "x-tkpd-pdpb": "0",
        "x-price-center": "true",
        "x-date": "Mon, 09 Mar 2026 12:58:38 +0700",
        "x-tkpd-akamai": "pdpMainInfo",
        "bd-device-id": "1334015120553134514",
        "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Cookie": "_abck=3A65C7B3B9B79098FF9D524358CA6EE5~-1~YAAQrPIiF+I07tCcAQAAOKQu0Q8nQGfUH86LRa/sowu19CscNQlcBilSWq0vxf1kZQUMoOR2P9pbxoi7jqkoDzENnqvRDJsD+KkGkM4/Njs4uwC98G4TEP5PtAJb3FFlwIdM8ypmhYiglz47biR8ElR6zC0BxcVfXyRKiwkGgvGkBIIpAjR8b+dGt6h2VtXzY0ATh/QY9bEajCuW0HvMWYl53dV8wlmcLjyPQGC3ZrbPDgAoG0wsTUpoJn00C4jwy708fmzxrdjr/IDisdqblFc8LdgGzVerAf4vRPly+SjFmN9WibEbEX658cGdhMaIfNmqhsQLKwKoPtQHSWwqTsNl8Si+4ebJS58R5S9zANdv7Ycul+mG5wTr35pMcDFo48WHySb+PxkEi0xbAcmuXTO22OwP5QrVIpHMV6ziO7FKbu3bLq6gfLBkN2f+qfnpPaTCllsxgC6vHw==~-1~-1~-1~-1~-1; ak_bmsc=871CDDC29D1366D6F32A68DA3ED4818E~000000000000000000000000000000~YAAQrPIiF+M07tCcAQAAOaQu0R8HOGpNH+wRuSpqYptbKxvaiV6wW0WUwxmTwgZXsM0tY2kS3hR4f18QdvCsLjT0tg9FmsKbTPdde+1ajubkbOowknK7bE+VG8RS7iSYKF92+KCe30rnkJ02jiMxQ744ATzagPhRGeZVo/8Km4TkUlnyIkX/cYnKcB9a6NeRJ+fw440EpfzgnZUPpbBYGzWxDWdJXXcyuqt7mNxGHQOJAju0AhvcKa0wJ1O74YK+PlYrbCOD5QGkqBN/svH65wraHl4NI/INMZ0n/TpUiO6B59Z3+k0QK9tQIa77b52hi/HtRa6BQSIRsurRqLlSJDldq29cNHn60nOXQXOEOtFs+Q==; bm_sz=8238D067115D38D3C257BA05E428DFD5~YAAQrPIiF+Q07tCcAQAAOaQu0R9rH6qOupDVFdb5P2utJUBBSYU9NzgS3auGprUXgqhrvjSqqg65JLQJq+O+51gRKjvqMKSaClPOkV2z8OXBFbmXj6etEdkixdn8p8+hqPRrtQJgreSCRe2MtXwgspivD4boQRC+bAkT3YWAD4NDMvfuxwyTsxgzTRA6mM5euRMjxOa4guY/mfnJ1yfSQveBdWg/EUaMMCYtMOLWho2Ji3ge8csbzTu6z9//sbRrIZYI56u34fCT0WpkI/wvS4Sx/QlOveFzdd6dM3Mr4wc0XRoIUX2XpI5GKZt1fEtFFuMGCmYPjwtHP3zhuVjHvxxGfbbc1JVq8KvKdo9oqBXCJiA=~4343362~3421763"
    }

def parse_tokopedia_url(url: str):
    try:
        path = urlparse(url).path.strip("/")
        parts = path.split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
        return None, None
    except:
        return None, None

def safe_get(obj, *keys):
    for k in keys:
        if obj is None:
            return None
        obj = obj.get(k)
    return obj

_session = requests.Session()

def get_product_info(shop, product_key):
    headers = get_headers()
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
        "query": """query PDPMainInfo($productKey: String, $shopDomain: String, $layoutID: String, $extraPayload: String, $queryParam: String, $source: String, $userLocation: pdpUserLocation) {
  pdpMainInfo(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, extraPayload: $extraPayload, queryParam: $queryParam, source: $source, userLocation: $userLocation) {
    data {
      basicInfo {
        alias
        shopName
        productID
        stats {
          countReview
          rating
        }
      }
    }
  }
}"""
    }]

    url = "https://gql.tokopedia.com/graphql/PDPMainInfo"
    try:
        r = _session.post(url, json=payload, headers=headers)
        data = r.json()
        print(f"DEBUG: product response: {data}")
        basic = safe_get(data[0], "data", "pdpMainInfo", "data", "basicInfo")
        if not basic or not basic.get("productID"):
            return None
        return {
            "productID": basic.get("productID"),
            "shopName": basic.get("shopName"),
            "productName": basic.get("alias"),
            "rating": safe_get(basic, "stats", "rating"),
            "reviewCount": safe_get(basic, "stats", "countReview")
        }
    except Exception as e:
        print(f"Error fetching product info: {e}")
        return None

def get_reviews(product_id, page=1, limit=50):
    headers = get_headers()
    # Adding second abck cookie if needed (user provided two in the curl)
    headers["Cookie"] += "; _abck=3A65C7B3B9B79098FF9D524358CA6EE5~-1~YAAQV/IiFwS7xs2cAQAAaCO81Q/8mGzv4A85zx8NjznU5K3d5y3ZjVDF/OeNoEL8gmBmzrtdhwOFZ1A+wwQhGW4LjHMr62xdjaLWz0qBlW1bpB7X7wBC4RCQp0ur4h53Cau3PbEAnPWDpIQFuMXDoCuGMfG/HcQVux1gnTRACsuTCEJTVZhXQcqZ7yKjhvPZg/o7m5xpXt4C9Dh/H1YJ4VVAbPKKIDc0PecL7FBA4dKMqZYe26D48IyX1sJkjQWvj8Dw4JkZYVylhZNMaqxeP/Dy+ltXQbBNHrQDF0nuxvf+o5GPEtbQluWLE5f91QenWF4CSg0mNEnmldNu852iqp/trbnNtotskQ+nFjub6ga+KS8B8MDKByOH5o6MfgKpRSqiryY3POrX31VOyr08wuvK+qQsEV+UnZN7cKeslPrHss/ax5D6YWU3zuFLJQ==~-1~-1~-1~-1~-1"
    
    payload = [{
        "operationName": "productReviewList",
        "variables": {
            "productID": str(product_id),
            "page": page,
            "limit": limit,
            "sortBy": "informative_score desc",
            "filterBy": ""
        },
        "query": """query productReviewList($productID: String!, $page: Int!, $limit: Int!, $sortBy: String, $filterBy: String) {
  productrevGetProductReviewList(productID: $productID, page: $page, limit: $limit, sortBy: $sortBy, filterBy: $filterBy) {
    list {
      id: feedbackID
      message
      productRating
    }
  }
}"""
    }]

    url = "https://gql.tokopedia.com/graphql/productReviewList"
    try:
        r = _session.post(url, json=payload, headers=headers)
        data = r.json()
        print(f"DEBUG: review response: {data}")
        reviews = safe_get(data[0], "data", "productrevGetProductReviewList", "list")
        return reviews or []
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []

def scrape_product(url):
    shop, product_key = parse_tokopedia_url(url)
    if not shop or not product_key:
        return None
    
    info = get_product_info(shop, product_key)
    if not info:
        return get_mock_data(url)
    
    product_id = info["productID"]
    reviews_data = get_reviews(product_id, page=1, limit=30)
    
    info["reviews"] = [r.get("message") for r in reviews_data if r.get("message")]
    return info

def get_mock_data(url):
    is_prod_1 = "1" in url or "a" in url
    return {
        "productID": str(random.randint(1000, 9999)),
        "shopName": "Official Store A" if is_prod_1 else "Gadget Store B",
        "productName": "Produk Premium X" if is_prod_1 else "Produk Unggulan Y",
        "rating": 4.8 if is_prod_1 else 4.5,
        "reviewCount": 150 if is_prod_1 else 200,
        "reviews": [
            "Barang sangat bagus, pengiriman cepat!",
            "Kualitas oke banget, puas belanja di sini.",
            "Respon penjual ramah, barang original.",
            "Agak kecewa sih pengiriman lama, tapi barang bagus.",
            "Packing rapi, sampai dengan selamat.",
            "Sesuai deskripsi, mantap joss!",
            "Gak nyesel beli di sini, keren!",
            "Harga murah tapi kualitas bukan murahan.",
            "Cepat sampai, terima kasih!",
            "Bagus sekali, berfungsi dengan baik."
        ],
        "is_mock": True
    }
