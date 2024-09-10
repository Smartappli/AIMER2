from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=FaqCategory.Status.PUBLISHED)


class PublishedQuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=FaqQuestion.Status.PUBLISHED)


class FaqCategory(models.Model):
    class Status(models.TextChoices):
        """Enumeration for category status."""

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
        SCHEDULED = "SC", "Scheduled"

    class Icon(models.TextChoices):
        """Enumeration for icon."""

        ACCESSIBILITY = "<i class='bx bx-accessibility'></i>", "Accessibility"
        ADJUST = "<i class='bx bx-adjust'></i>", "Adjust"
        ANCHOR = "<i class='bx bx-anchor'></i>", "Anchor"
        ALARM = "<i class='bx bx-alarm'></i>", "Alarm"
        APERTURE = "<i class='bx bx-aperture'></i>", "Aperture"
        ARCHIVE = "<i class='bx bx-archive'></i>", "Archive"
        AT = "<i class='bx bx-at'></i>", "At"
        AWARD = "<i class='bx bx-award'></i>", "Award"
        BADGE = "<i class='bx bx-badge'></i>", "Badge"
        BAR_CHART = "<i class='bx bx-chart'></i>", "Bar Chart"
        BATTERY = "<i class='bx bx-battery'></i>", "Battery"
        BELL = "<i class='bx bx-bell'></i>", "Bell"
        BLOCK = "<i class='bx bx-block'></i>", "Block"
        BLUETOOTH = "<i class='bx bx-blue'></i>", "Bluetooth"
        BODY = "<i class='bx bx-body'></i>", "Body"
        BONG = "<i class='bx bx-bond'></i>", "Bond"
        BOOKMARK = "<i class='bx bx-bookmark'></i>", "Bookmark"
        BRAILLE = "<i class='bx bx-braille' ></i>", "Braille"
        BUG = "<i class='bx bx-bug'></i>", "Bug"
        BULB = "<i class='bx bx-bulb'></i>", "Bulb"
        BROADCAST = "<i class='bx bx-broadcast'></i>", "Broadcast"
        BUILDINGS = "<i class='bx bx-buildings'></i>", "Buildings"
        BRIEFCASE = "<i class='bx bx-briefcase'></i>", "Briefcase"
        BRUSH = "<i class='bx bx-brushes'></i>", "Brush"
        CALENDAR = "<i class='bx bx-calendar'></i>", "Calendar"
        CAMERA = "<i class='bx bx-camera'></i>", "Camera"
        CAPSULE = "<i class='bx bx-capsule'></i>", "Capsule"
        CARD = "<i class='bx bx-card'></i>", "Card"
        CATEGORY = "<i class='bx bx-category'></i>", "Category"
        CHECK = "<i class='bx bx-check'></i>", "Check"
        CHIP = "<i class='bx bx-chip'></i>", "Chip"
        CLOUD = "<i class='bx bx-cloud'></i>", "Cloud"
        CODE = "<i class='bx bx-code'></i>", "Code"
        COG = "<i class='bx bx-cog'></i>", "Cog"
        COLLECTION = "<i class='bx bx-collection'></i>", "Collection"
        COPY = "<i class='bx bx-copy'></i>", "Copy"
        CROP = "<i class='bx bx-crop'></i>", "Crop"
        CUBE = "<i class='bx bx-cube'></i>", "Cube"
        CUT = "<i class='bx bx-cut'></i>", "Cut"
        DATA = "<i class='bx bx-data'></i>", "Data"
        DESKTOP = "<i class='bx bx-desktop'></i>", "Desktop"
        DETAIL = "<i class='bx bx-detail'></i>", "Detail"
        DIRECTIONS = "<i class='bx bx-directions'></i>", "Directions"
        DNA = "<i class='bx bx-dna'></i>", "DNA"
        DUPLICATE = "<i class='bx bx-duplicate'></i>", "Duplicate"
        EDIT = "<i class='bx bx-edit'></i>", "Edit"
        ERASER = "<i class='bx bx-eraser'></i>", "Eraser"
        EXPAND = "<i class='bx bx-expand ></i>", "Expand"
        EXPORT = "<i class='bx bx-export'></i>", "Export"
        FILE = "<i class='bx bx-file'></i>", "File"
        FILTER = "<i class='bx bx-filter'></i>", "Filter"
        FLAG = "<i class='bx bx-flag'></i>", "Flag"
        GIFT = "<i class='bx bx-gift'></i>", "Gift"
        GLOBE = "<i class='bx bx-global'></i>", "Globe"
        GROUP = "<i class='bx bx-group'></i>", "Group"
        HASH = "<i class='bx bx-hash'></i>", "Hash"
        HDD = "<i class='bx bx-hdd'></i>", "HDD"
        HEART = "<i class='bx bx-heart'></i>", "Heart"
        HOME = "<i class='bx bx-home'></i>", "Home"
        HISTORY = "<i class='bx bx-history'></i>", "History"
        ID_CARD = "<i class='bx bx-id-card'></i>", "ID Card"
        IMAGES = "<i class='bx bx-images'></i>", "Images"
        INJECTION = "<i class='bx bx-injection'></i>", "Injection"
        KEY = "<i class='bx bx-key'></i>", "Key"
        LAPTOP = "<i class='bx bx-laptop'></i>", "Laptop"
        LAYER = "<i class='bx bx-layer'></i>", "Layer"
        LEMON = "<i class='bx bx-lemon'></i>", "Lemon"
        LIBRARY = "<i class='bx bx-library'></i>", "Library"
        LINE_CHART = "<i class='bx bx-line-chart'></i>", "Line-Chart"
        LOCK = "<i class='bx bx-lock'></i>", "Lock"
        MAGNET = "<i class='bx bx-magnet'></i>", "Magnet"
        MAP = "<i class='bx bx-map'></i>", "Map"
        MENU = "<i class='bx bx-menu'></i>", "Menu"
        MICROCHIP = "<i class='bx bx-microchip'></i>", "Microchip"
        MOBILE = "<i class='bx bx-mobile'></i>", "Mobile"
        MOON = "<i class='bx bx-moon'></i>", "Moon"
        NAVIGATION = "<i class='bx bx-nav'></i>", "Navigation"
        NEWS = "<i class='bx bx-news'></i>", "News"
        OUTLINE = "<i class='bx bx-outline'></i>", "Outline"
        PACKAGE = "<i class='bx bx-package'></i>", "Package"
        PAINT = "<i class='bx bx-paint'></i>", "Paint"
        PASTE = "<i class='bx bx-paste'></i>", "Paste"
        PIN = "<i class='bx bx-pin'></i>", "Pin"
        PENCIL = "<i class='bx bx-pencil'></i>", "Pencil"
        PHONE = "<i class='bx bx-phone'></i>", "Phone"
        PIE_CHART = "<i class='bx bx-pie'></i>", "Pie Chart"
        PRINTER = "<i class='bx bx-printer'></i>", "Printer"
        PULSE = "<i class='bx bx-pulse'></i>", "Pulse"
        QUESTION_MARK = "<i class='bx bx-question-mark'></i>", "Question-Mark"
        RECYCLE = "<i class='bx bx-recycle'></i>", "Recycle"
        REFRESH = "<i class='bx bx-refresh'></i>", "Refresh"
        REPEAT = "<i class='bx bx-repeat'></i>", "Repeat"
        RSS = "<i class='bx bx-rss'></i>", "Rss"
        RULER = "<i class='bx bx-ruler'></i>", "Ruler"
        SEND = "<i class='bx bx-send'></i>", "Send"
        SEARCH = "<i class='bx bx-search'></i>", "Search"
        SERVER = "<i class='bx bx-server'></i>", "Server"
        SHIELD = "<i class='bx bx-shield'></i>", "Shield"
        SHUFFLE = "<i class='bx bx-shuffle'></i>", "Shuffle"
        SIDEBAR = "<i class='bx bx-sidebar'></i>", "Sidebar"
        SITEMAP = "<i class='bx bx-sitemap'></i>", "SiteMap"
        SLIDER = "<i class='bx bx-slider'></i>", "Slider"
        SORT = "<i class='bx bx-sort'></i>", "Sort"
        SPEAKER = "<i class='bx bx-speaker'></i>", "Speaker"
        SPREADSHEET = "<i class='bx bx-spreadsheet'></i>", "Spreadsheet"
        STATION = "<i class='bx bx-station'></i>", "Station"
        STOP = "<i class='bx bx-stop'></i>", "Stop"
        STOPWATCH = "<i class='bx bx-stopwatch'></i>", "StopWatch"
        SUPPORT = "<i class='bx bx-support'></i>", "Support"
        SYNC = "<i class='bx bx-sync'></i>", "Sync"
        TABLE = "<i class='bx bx-table'></i>", "Table"
        TASK = "<i class='bx bx-task'></i>", "Task"
        TERMINAL = "<i class='bx bx-terminal'></i>", "Terminal"
        TIME = "<i class='bx bx-time'></i>", "Time"
        TRASH = "<i class='bx bx-trash'></i>", "Trash"
        TRIP = "<i class='bx bx-trip'></i>", "Trip"
        TROPHY = "<i class='bx bx-trophy'></i>", "Trophy"
        UNIVERSAL_ACCESS = (
            "<i class='bx bx-universal-access' ></i>",
            "Universal Access",
        )
        UPLOAD = "<i class='bx bx-upload'></i>", "Upload"
        USB = "<i class='bx bx-usb'></i>", "USB"
        VIAL = "<i class='bx bx-vial'></i>", "Vial"
        VIDEO = "<i class='bx bx-video'></i>", "Video"
        VOICEMAIL = "<i class='bx bx-voicemail'></i>", "Voicemail"
        VOLUME = "<i class='bx bx-volume'></i>", "Volume"
        WINDOWS = "<i class='bx bx-windows'></i>", "Windows"
        WIFI = "<i class='bx bx-wifi'></i>", "WiFi"
        WRENCH = "<i class='bx bx-wrench'></i>", "Wrench"

    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=150,
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
    slug = models.SlugField(max_length=250, unique=True)
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

    published = PublishedQuestionManager()
    tags = TaggableManager()

    def __str__(self) -> str:
        return self.title
