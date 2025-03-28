from collections import namedtuple

Position = namedtuple("position", ["y", "x"])
warn_position = Position(0, 0)  # duplicate project & refresh time
SortPlaceHolder = namedtuple("sort_place_holder", ["place_holder", "sorted_key"])
lucy = SortPlaceHolder("@1", ['tkl-pom', 'tkl-core', 'tkl-component', 'tkl-cms-api', 'tkl-user-api', 'tkl-tool-api',
                              'tkl-base-api', 'tkl-sport-core', 'tkl-sport-adapter-api', 'tkl-sport-data-api',
                              'tkl-sport-risk-api', 'tkl-offline-api', 'tkl-wallet-api', 'tkl-pay-api', 'tkl-order-api',
                              'tkl-rec-api', 'tkl-sport-bet-api', 'tkl-module-starter', 'tkl-open-sdk',
                              'tkl-search-api', 'tkl-event-api', 'tkl-game-api', 'tkl-lotto-api', 'tkl-common-business',
                              'tkl-cms-service', 'tkl-dis-api', 'tkl-user-service', 'tkl-statistics-api',
                              'tkl-wallet-service', 'tkl-order-service', 'tkl-search-service', 'tkl-sport-bet-service',
                              'tkl-lotto', 'tkl-statistics', 'tkl-event', 'tkl-pay', 'tkl-platform-engine', 'tkl-game',
                              'tkl-archive', 'tkl-tool-service', 'tkl-data', 'tkl-data-api', 'tkl-sale-api',
                              'tkl-sport-bet-engine', 'tkl-agent-api', 'tkl-agent-manager', 'tkl-lottery-manager',
                              'tkl-game-manager', 'tkl-message', 'tkl-h5-api', 'tkl-open-api', 'tkl-gateway'])

__sorted_key_map = {lucy.place_holder: lucy.sorted_key}


def get_by_key(sorted_key):
    result = __sorted_key_map.get(sorted_key)
    if result:
        return result
    return [] if not sorted_key else sorted_key.split(",")


if __name__ == "__main__":
    print(get_by_key("@1"))
