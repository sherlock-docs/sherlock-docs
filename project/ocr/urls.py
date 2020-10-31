from rest_framework.routers import SimpleRouter
from .views import DocumentView, DocumentTypeView

router = SimpleRouter(trailing_slash=False)
router.register('document', DocumentView, basename='document')
router.register('document_type', DocumentTypeView, basename='document_type')

urlpatterns = router.urls
