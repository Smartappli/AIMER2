from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedCategoryManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=FaqCategory.Status.PUBLISHED)
        )


class PublishedQuestionManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=FaqQuestion.Status.PUBLISHED)
        )


class FaqCategory(models.Model):
    class Status(models.TextChoices):
        """Enumeration for category status."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        SCHEDULED = "SC", "Scheduled"

    class Icon(models.TextChoices):
        """Enumeration for icon."""

        ACCESSIBILITY = "bx bx-accessibility", "Accessibility"
        ADJUST = "bx bx-adjust", "Adjust"
        ANCHOR = "bx bx-anchor", "Anchor"
        ALARM = "bx bx-alarm", "Alarm"
        APERTURE = "bx bx-aperture", "Aperture"
        ARCHIVE = "bx bx-archive", "Archive"
        AT = "bx bx-at", "At"
        AWARD = "bx bx-award", "Award"
        BADGE = "bx bx-badge", "Badge"
        BAR_CHART = "bx bx-chart", "Bar Chart"
        BATTERY = "bx bx-battery", "Battery"
        BELL = "bx bx-bell", "Bell"
        BLOCK = "bx bx-block", "Block"
        BLUETOOTH = "bx bx-blue", "Bluetooth"
        BODY = "bx bx-body", "Body"
        BONG = "bx bx-bond", "Bond"
        BOOKMARK = "bx bx-bookmark", "Bookmark"
        BRAILLE = "bx bx-braille", "Braille"
        BUG = "bx bx-bug", "Bug"
        BULB = "bx bx-bulb", "Bulb"
        BROADCAST = "bx bx-broadcast", "Broadcast"
        BUILDINGS = "bx bx-buildings", "Buildings"
        BRIEFCASE = "bx bx-briefcase", "Briefcase"
        BRUSH = "bx bx-brushes", "Brush"
        CALENDAR = "bx bx-calendar", "Calendar"
        CAMERA = "bx bx-camera", "Camera"
        CAPSULE = "bx bx-capsule", "Capsule"
        CARD = "bx bx-card", "Card"
        CATEGORY = "bx bx-category", "Category"
        CHECK = "bx bx-check", "Check"
        CHIP = "bx bx-chip", "Chip"
        CLOUD = "bx bx-cloud", "Cloud"
        CODE = "bx bx-code", "Code"
        COG = "bx bx-cog", "Cog"
        COLLECTION = "bx bx-collection", "Collection"
        COPY = "bx bx-copy", "Copy"
        CROP = "bx bx-crop", "Crop"
        CUBE = "bx bx-cube", "Cube"
        CUT = "bx bx-cut", "Cut"
        DATA = "bx bx-data", "Data"
        DESKTOP = "bx bx-desktop", "Desktop"
        DETAIL = "bx bx-detail", "Detail"
        DIRECTIONS = "bx bx-directions", "Directions"
        DNA = "bx bx-dna", "DNA"
        DUPLICATE = "bx bx-duplicate", "Duplicate"
        EDIT = "bx bx-edit", "Edit"
        ERASER = "bx bx-eraser", "Eraser"
        EXPAND = "bx bx-expand", "Expand"
        EXPORT = "bx bx-export", "Export"
        FILE = "bx bx-file", "File"
        FILTER = "bx bx-filter", "Filter"
        FLAG = "bx bx-flag", "Flag"
        GIFT = "bx bx-gift", "Gift"
        GLOBE = "bx bx-global", "Globe"
        GROUP = "bx bx-group", "Group"
        HASH = "bx bx-hash", "Hash"
        HDD = "bx bx-hdd", "HDD"
        HEART = "bx bx-heart", "Heart"
        HOME = "bx bx-home", "Home"
        HISTORY = "bx bx-history", "History"
        ID_CARD = "bx bx-id-card", "ID Card"
        IMAGES = "bx bx-images", "Images"
        INJECTION = "bx bx-injection", "Injection"
        KEY = "bx bx-key", "Key"
        LAPTOP = "bx bx-laptop", "Laptop"
        LAYER = "bx bx-layer", "Layer"
        LEMON = "bx bx-lemon", "Lemon"
        LIBRARY = "bx bx-library", "Library"
        LINE_CHART = "bx bx-line-chart", "Line-Chart"
        LOCK = "bx bx-lock", "Lock"
        MAGNET = "bx bx-magnet", "Magnet"
        MAP = "bx bx-map", "Map"
        MENU = "bx bx-menu", "Menu"
        MICROCHIP = "bx bx-microchip", "Microchip"
        MOBILE = "bx bx-mobile", "Mobile"
        MOON = "bx bx-moon", "Moon"
        NAVIGATION = "bx bx-nav", "Navigation"
        NEWS = "bx bx-news", "News"
        OUTLINE = "bx bx-outline", "Outline"
        PACKAGE = "bx bx-package", "Package"
        PAINT = "bx bx-paint", "Paint"
        PASTE = "bx bx-paste", "Paste"
        PIN = "bx bx-pin", "Pin"
        PENCIL = "bx bx-pencil", "Pencil"
        PHONE = "bx bx-phone", "Phone"
        PIE_CHART = "bx bx-pie", "Pie Chart"
        PRINTER = "bx bx-printer", "Printer"
        PULSE = "bx bx-pulse", "Pulse"
        QUESTION_MARK = "bx bx-question-mark", "Question-Mark"
        RECYCLE = "bx bx-recycle", "Recycle"
        REFRESH = "bx bx-refresh", "Refresh"
        REPEAT = "bx bx-repeat", "Repeat"
        RSS = "bx bx-rss", "Rss"
        RULER = "bx bx-ruler", "Ruler"
        SEND = "bx bx-send", "Send"
        SEARCH = "bx bx-search", "Search"
        SERVER = "bx bx-server", "Server"
        SHIELD = "bx bx-shield", "Shield"
        SHUFFLE = "bx bx-shuffle", "Shuffle"
        SIDEBAR = "bx bx-sidebar", "Sidebar"
        SITEMAP = "bx bx-sitemap", "SiteMap"
        SLIDER = "bx bx-slider", "Slider"
        SORT = "bx bx-sort", "Sort"
        SPEAKER = "bx bx-speaker", "Speaker"
        SPREADSHEET = "bx bx-spreadsheet", "Spreadsheet"
        STATION = "bx bx-station", "Station"
        STOP = "bx bx-stop", "Stop"
        STOPWATCH = "bx bx-stopwatch"
        SUPPORT = "bx bx-support", "Support"
        SYNC = "bx bx-sync", "Sync"
        TABLE = "bx bx-table", "Table"
        TASK = "bx bx-task", "Task"
        TERMINAL = "bx bx-terminal", "Terminal"
        TIME = "bx bx-time", "Time"
        TRASH = "bx bx-trash", "Trash"
        TRIP = "bx bx-trip", "Trip"
        TROPHY = "bx bx-trophy", "Trophy"
        UNIVERSAL_ACCESS = (
            "bx bx-universal-access",
            "Universal Access",
        )
        UPLOAD = "bx bx-upload", "Upload"
        USB = "bx bx-usb", "USB"
        VIAL = "bx bx-vial", "Vial"
        VIDEO = "bx bx-video", "Video"
        VOICEMAIL = "bx bx-voicemail", "Voicemail"
        VOLUME = "bx bx-volume", "Volume"
        WINDOWS = "bx bx-windows", "Windows"
        WIFI = "bx bx-wifi", "WiFi"
        WRENCH = "bx bx-wrench", "Wrench"

    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, default="")
    icon = models.CharField(
        max_length=50,
        choices=Icon.choices,
        default=Icon.ACCESSIBILITY,
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    published = PublishedCategoryManager()

    def __str__(self) -> str:
        return self.name


class FaqQuestion(models.Model):
    class Status(models.TextChoices):
        """Enumeration for category status."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        SCHEDULED = "SC", "Scheduled"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, default="")
    category = models.ForeignKey(
        FaqCategory,
        on_delete=models.CASCADE,
        related_name="faq_category",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="faq_author",
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    published = PublishedCategoryManager()
    published2 = PublishedQuestionManager()
    tags = TaggableManager()

    def __str__(self) -> str:
        return self.title
