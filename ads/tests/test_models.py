# tests/test_models.py
import pytest
from ads.models import Ad, ExchangeProposal

@pytest.mark.django_db
def test_ad_creation(ad):
    assert ad.title == 'Test Ad'
    assert ad.status == 'active'
    assert str(ad) == 'Test Ad (Электроника)'

@pytest.mark.django_db
def test_proposal_creation(proposal):
    assert proposal.status == 'pending'
    assert 'Test Proposal' in str(proposal)