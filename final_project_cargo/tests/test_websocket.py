from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator

from rest_framework_simplejwt.tokens import AccessToken

import pytest

from final_project_app.routing import application

from final_project_cargo.models import Send_cargo

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


PASSWORD = 'Aa231111111114'


class AuthenticationTest(APITestCase):

    def test_user_can_sign_up(self):

        response = self.client.post(reverse('sign_up'), data={
            'email': '1@gggg.com',
            'phone_number': '1233211233',

            'first_name': 'Test',
            'last_name': 'User',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'group': 'rider',
            'image': '',


        },)
        user = get_user_model().objects.last()
        res = response.data

        assert res['first_name'] == 'Test'
        assert res['last_name'] == 'User'
        assert res['group'] == 'rider'
        assert res['email'] == '1@gggg.com'
        assert res['phone_number'] == '1233211233'

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertIsNotNone(user.image)


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@database_sync_to_async
def create_user(
    email,
    password,
    group='rider'
):
    # Create user.
    user = get_user_model().objects.create_user(
        username=email,
        email=email,
        password=password
    )

    # Create user group.
    user_group, _ = Group.objects.get_or_create(name=group)
    user.groups.add(user_group)
    user.save()

    # Create access token.
    access = AccessToken.for_user(user)

    return user, access


@database_sync_to_async
def create_trip(
    pick_up_address='cho ben thanh',
    drop_off_address='cho tan dinh',
    cargo_weight=10,
    cargo_note='None',
    get_cargo_name='aloal43o',
    phone_number_get_cargo='09999919237',
    cargo_price='12000',
    cargo_distance=10,
    status='REQUESTED',
    rider=None,
    driver=None
):
    return Send_cargo.objects.create(

        pick_up_address=pick_up_address,
        drop_off_address=drop_off_address,
        cargo_weight=cargo_weight,
        cargo_note=cargo_note,
        get_cargo_name=get_cargo_name,
        phone_number_get_cargo=phone_number_get_cargo,
        cargo_price=cargo_price,
        cargo_distance=cargo_distance,
        status=status,
        rider=rider,
        driver=driver
    )


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'this is pass'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'test.user@example.com', 'this is pass'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/taxi/'
        )
        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()

    async def test_join_driver_pool(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_user(
            'user@gmails.com', 'this is pass', 'driver'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('drivers', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_request_trip(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user(
            'user@gmail.com', 'this is pass', 'rider'
        )
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/taxi/?token={access}'
        )
        connected, _ = await communicator.connect()
        await communicator.send_json_to({
            'type': 'create.trip',
            'data': {
                'pick_up_address': 'cho ben thanh',
                'drop_off_address': 'cho tan dinh',
                'cargo_weight': 10,
                'cargo_note': 'None',
                'get_cargo_name': 'aloal43o',
                'phone_number_get_cargo': '09999919237',
                'cargo_price': '12000',
                'cargo_distance': 10,
                'rider': user.id,
            },
        })
        response = await communicator.receive_json_from()
        response_data = response.get('data')
        assert response_data['id'] is not None
        assert response_data['pick_up_address'] == 'cho ben thanh'
        assert response_data['drop_off_address'] == 'cho tan dinh'
        assert response_data['cargo_weight'] == 10
        assert response_data['cargo_note'] == 'None'
        assert response_data['get_cargo_name'] == 'aloal43o'
        assert response_data['phone_number_get_cargo'] == '09999919237'
        assert response_data['cargo_price'] == '12000'
        assert response_data['cargo_distance'] == 10
        assert response_data['status'] == 'REQUESTED'
        assert response_data['rider']['email'] == user.email
        assert response_data['driver'] is None
        await communicator.disconnect()
