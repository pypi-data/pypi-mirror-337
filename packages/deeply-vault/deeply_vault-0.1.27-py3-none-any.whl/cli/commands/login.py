import click
import requests

from cli.utils.config import get_config, save_config
from cli.utils.token import save_token


@click.command()
@click.option("--server", "-s", help="서버 URL")
@click.option("--api-key", "-k", help="API 키로 로그인 (CI/CD 환경용)")
@click.option("--username", "-u", help="사용자명 (비밀번호만 입력받음)")
def login(server, api_key, username):
    """서버에 로그인

    API 인증 토큰을 발급받고 저장합니다.
    사용자명/비밀번호 또는 API 키로 로그인할 수 있습니다.
    """
    try:
        # 설정 파일 읽기
        config = get_config()

        if server:
            config["server"] = server

        server_url = config.get("server")

        if not server_url:
            click.echo(
                "서버 URL이 설정되지 않았습니다. 명령어 예시: deeply login -s http://localhost:13500")
            return

        # 토큰 발급 요청
        if api_key:
            # API 키로 로그인 (CI/CD 환경)
            response = requests.post(
                f"{server_url}/api/v1/auth/token",
                json={"api_key": api_key}
            )
        elif username:
            # 사용자명이 제공된 경우 비밀번호만 입력받음
            password = click.prompt("비밀번호", hide_input=True)
            response = requests.post(
                f"{server_url}/api/v1/auth/token",
                data={"username": username, "password": password}
            )
        else:
            # 대화형 로그인
            auth_method = click.prompt(
                "로그인 방식을 선택하세요",
                type=click.Choice(["1", "2"]),
                default="1",
                show_choices=False,
                prompt_suffix="\n1. 사용자명/비밀번호\n2. API 키\n선택: "
            )

            if auth_method == "2":
                # API 키로 로그인
                api_key = click.prompt("API 키", hide_input=True)
                response = requests.post(
                    f"{server_url}/api/v1/auth/token",
                    json={"api_key": api_key}
                )
            else:
                # 사용자명/비밀번호로 로그인
                username = click.prompt("사용자명")
                password = click.prompt("비밀번호", hide_input=True)
                
                response = requests.post(
                    f"{server_url}/api/v1/auth/token",
                    data={"username": username, "password": password}
                )

        if response.status_code != 200:
            click.echo(
                f"로그인 실패: {response.json().get('detail', '알 수 없는 오류')}", err=True)
            return

        # 토큰 저장
        token_data = response.json()
        token = token_data.get("access_token")
        save_token(token)

        # 설정 파일 업데이트 (토큰 제외)
        save_config(config)

        click.echo("Vault 로그인 성공! API 토큰이 ~/.deeply/vault/token.json에 저장되었습니다.")

    except Exception as e:
        click.echo(f"오류가 발생했습니다: {str(e)}", err=True)
