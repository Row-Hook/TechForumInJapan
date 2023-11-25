from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Pages

class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバーライドした独自TestCaseクラス"""

    def setUp(self):
        """テストメソッド実行前の事前設定"""
        #テストユーザーのパスワード
        self.password='Iamcool1@'

        #各インスタンスメソッドで使うテスト用ユーザーを生成し
        #インスタンス変数に格納しておく
        self.test_user= get_user_model().objects.create_user(
            username='test_user1',
            email="hookhamrowan@gmail.com",
            password=self.password)

        #テスト用ユーザーでログインする
        self.client.login(email=self.test_user.email, password=self.password)

class TestPagesCreateView(LoggedInTestCase):
    """PagesCreateView用のテストクラス"""

    def test_create_pages_success(self):
        """ページ作成処理が成功することを検証する"""

        #Postパラメータ
        params = {'title':'テストタイトル',
                  'content':'本文',
                  'photo1':'',
                  'photo2':'',
                  'photo3':''}

        #新規ページ作成処理(Post)を実行
        response = self.client.post(reverse_lazy('pages:pages_create'), params)

        #ページ一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('pages:pages_list'))

        #ページデータがデータベースに登録されたかを検証
        self.assertEqual(Pages.objects.filter(title='テストタイトル').count(),1)

    def test_create_pages_failure(self):
        """新規ページ作成処理が失敗することを検証する"""

        #新規ページ作成処理(Post)を実行
        response = self.client.post(reverse_lazy('pages:pages_create'))

        #必須フォームフィールドが未入力によりエラーになることを検証
        self.assertFormError(response, 'form','title','このフィールドは必須です。')

class TestPagesUpdateView(LoggedInTestCase):
    """PagesUpdateView用のテストクラス"""

    def test_update_pages_succces(self):
        """ページ編集処理が成功することを検証する"""

        #テスト用ページデータの作成
        pages= Pages.objects.create(user=self.test_user, title='タイトル編集前')

        #Postパラメータ
        params={'title':'タイトル編集後'}

        #ページ編集処理(Post)を実行
        response= self.client.post(reverse_lazy('pages:pages_update', kwargs={'pk': pages.pk}), params)

        #ページ詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('pages:pages_detail', kwargs={'pk': pages.pk}))

        #ページデータが編集されたかを検証
        self.assertEqual(Pages.objects.get(pk=pages.pk).title, 'タイトル編集後')

    def test_update_pages_failure(self):
        """ページ編集処理が失敗することを検証する"""

        # ページ編集処理(Post)を実行
        response = self.client.post(reverse_lazy('pages:pages_update', kwargs={'pk':999}))

        # 存在しないページデータを編集しようとしてエラーになることを検証
        self.assertEqual(response.status_code,404)

class TestPagesDeleteView(LoggedInTestCase):
    """PagesDeleteView用のテストクラス"""

    def test_delete_pages_success(self):
        """PagesDeleteView用のテストクラス"""

        #テスト用ページデータの作成
        pages=Pages.objects.create(user=self.test_user, title='タイトル')

        #ページ削除処理(Post)を実行
        response= self.client.post(reverse_lazy('pages:pages_delete',kwargs={'pk':pages.pk}))

        #ページ一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('pages:pages_list'))

        #ページデータが削除されたかを検証
        self.assertEqual(Pages.objects.filter(pk=pages.pk).count(),0)

    def test_delete_pages_failure(self):
        """ページ削除処理が失敗することを検証する"""

        #ページ削除処理(Post)を実行
        response = self.client.post(reverse_lazy('pages:pages_delete',kwargs={'pk':999}))

        #存在しないページデータを削除しようとしてエラーになることを検証
        self.assertEqual(response.status_code, 404)