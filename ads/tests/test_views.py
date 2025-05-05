# import pytest
# from django.urls import reverse
#
# @pytest.mark.django_db
# class TestAdAPI:
#     def test_create_ad(self, auth_client):
#         url = reverse('ad-list')
#         data = {
#             'title': 'New Ad',
#             'description': 'New Description',
#             'category': 'books',
#             'condition': 'used'
#         }
#         response = auth_client.post(url, data)
#         assert response.status_code == 201
#         assert response.data['title'] == 'New Ad'
#
#     def test_retrieve_ad(self, auth_client, ad):
#         url = reverse('ad-detail', args=[ad.id])
#         response = auth_client.get(url)
#         assert response.status_code == 200
#         assert response.data['title'] == 'Test Ad'
#
#     def test_update_ad(self, auth_client, ad):
#         url = reverse('ad-detail', args=[ad.id])
#         data = {'title': 'Updated Title'}
#         response = auth_client.patch(url, data)
#         assert response.status_code == 200
#         ad.refresh_from_db()
#         assert ad.title == 'Updated Title'
#
#     def test_delete_ad(self, auth_client, ad):
#         url = reverse('ad-detail', args=[ad.id])
#         response = auth_client.delete(url)
#         assert response.status_code == 204
#         assert Ad.objects.count() == 0
#
#     def test_search_ads(self, auth_client, ad):
#         url = reverse('ad-list') + '?q=Test'
#         response = auth_client.get(url)
#         assert response.status_code == 200
#         assert len(response.data['results']) == 1
#
# @pytest.mark.django_db
# class TestProposalAPI:
#     def test_create_proposal(self, auth_client, ad):
#         receiver_ad = Ad.objects.create(
#             user=auth_client.user,
#             title='Receiver Ad',
#             description='Test'
#         )
#         url = reverse('proposal-list')
#         data = {
#             'ad_sender': ad.id,
#             'ad_receiver': receiver_ad.id,
#             'comment': 'Test Proposal'
#         }
#         response = auth_client.post(url, data)
#         assert response.status_code == 201
#         assert response.data['comment'] == 'Test Proposal'
#
#     def test_own_ad_proposal(self, auth_client, ad):
#         url = reverse('proposal-list')
#         data = {
#             'ad_sender': ad.id,
#             'ad_receiver': ad.id,
#             'comment': 'Invalid'
#         }
#         response = auth_client.post(url, data)
#         assert response.status_code == 400
#
#     def test_update_proposal_status(self, auth_client, proposal):
#         url = reverse('proposal-detail', args=[proposal.id])
#         data = {'status': 'accepted'}
#         response = auth_client.patch(url, data)
#         assert response.status_code == 200
#         proposal.refresh_from_db()
#         assert proposal.status == 'accepted'
#
#     def test_unauthorized_access(self, api_client):
#         url = reverse('proposal-list')
#         response = api_client.get(url)
#         assert response.status_code == 403