def parse_handle(handle):
    for r in ["http://", "https://", "www.twitter.com/", "twitter.com/", "@"]:
        handle = handle.replace(r, "")
    return handle
