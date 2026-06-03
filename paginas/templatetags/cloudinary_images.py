from django import template

register = template.Library()


def _cloudinary_transform(url, transformation):
    if not url:
        return ""

    url = str(url)

    if "res.cloudinary.com" not in url or "/upload/" not in url:
        return url

    if f"/upload/{transformation}/" in url:
        return url

    return url.replace("/upload/", f"/upload/{transformation}/", 1)


@register.filter
def cloudinary_feed(url):
    return _cloudinary_transform(url, "f_auto,q_auto,c_limit,w_1100")


@register.filter
def cloudinary_thumb(url):
    return _cloudinary_transform(url, "f_auto,q_auto,c_fill,w_420,h_420")


@register.filter
def cloudinary_avatar(url):
    return _cloudinary_transform(url, "f_auto,q_auto,c_fill,g_face,w_160,h_160")
