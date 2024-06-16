import PySimpleGUI as sg
import subprocess
import threading
import time
import pexpect

class GUI:
    def __init__(self):
        # ウィンドウの初期化時にfinalize=Trueを追加
        self.window = sg.Window("Nord_VPN_GUI", self.get_layout(), resizable=True, finalize=True)
        self.running = True  # スレッドの停止を管理するためのフラグ

        # アプリケーションの初期化時にオプションをすべてONに設定する
        self.initial_setup()

    def get_layout(self):
        # 接続タブの内容
        接続タブ = [
            [sg.Text("Nord_VPN_GUI", size=(15, 1))],
            [sg.Text("コネクト", size=(10, 1)), sg.Button("最寄りのスタンダードサーバー", key="-最寄りのスタンダードサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("P2Pサーバー", key="-P2Pサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("ダブルVPNサーバー", key="-ダブルVPNサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("Onion Over VPNサーバー", key="-Onion_Over_VPNサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("Dedicated IPサーバー", key="-Dedicated_IPサーバー-")],
            [sg.Text("        ", size=(10, 1)), sg.Button("Obfuscatedサーバー", key="-Obfuscatedサーバー-")],
            [sg.Text("", size=(10, 1)), sg.Button("ログイン", key="-ログイン-"), sg.Button("切断", key="-切断-"), sg.Button("ログアウト", key="-ログアウト-")]
        ]

        # オプションタブの内容
        オプションタブ = [
            [sg.Text("オプション")],
            [sg.Checkbox("脅威防御ライト", True, key="-脅威防御ライト-")],
            [sg.Checkbox("キルスイッチ", True, key="-キルスイッチ-")],
            [sg.Checkbox("自動接続", True, key="-自動接続-")],
            [sg.Checkbox("通知", True, key="-通知-")],
            [sg.Checkbox("混乱化", True, key="-混乱化-")],
            [sg.Checkbox("メッシュネット", True, key="-メッシュネット-")]
        ]

        # ステータスタブの内容
        ステータス = [
            [sg.Text("ステータス")],
            [sg.Text("", key="-ステータス-", size=(50, 1))]
        ]

        # 設定タブの内容
        設定タブ = [
            [sg.Text("設定")],
            [sg.Button("インストール"), sg.Input("sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)", key='-インストール-', size=(50, 1))],
            [sg.Button("systemctl enable nordvpnd", key="systemctl_enable"),],
            [sg.Button("systemctl start nordvpnd", key="systemctl_start")],
            [sg.Button("systemctl stop nordvpnd", key="systemctl_stop")],
            [sg.Button("systemctl disable nordvpnd", key="systemctl_disable")],
            [sg.Button("systemctl status nordvpnd", key="systemctl_status")],
            [sg.Button("systemctl restart nordvpnd", key="systemctl_restart")],
            [sg.Input("", key="port_add"), sg.Button("ポートの開放")],
            [sg.Input("", key="port_remove"), sg.Button("ポートを閉じる")]
        ]

        # タブグループの作成
        tab_group = sg.TabGroup([
            [sg.Tab('接続', 接続タブ), sg.Tab('オプション', オプションタブ), sg.Tab('設定', 設定タブ)]
        ])

        # レイアウトにタブグループを追加
        layout = [
            [tab_group],
            [ステータス]
        ]

        return layout

    def update_status(self, message):
        self.window['-ステータス-'].update(message)

    def run_command(self, command):
        if command.startswith("sudo"):
            child = pexpect.spawn(command)
            child.expect('ban')  # パスワードプロンプトを期待
            child.sendline('aniki1119')  # パスワードを送信
            child.wait()
            return child.before.decode('utf-8')
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr

    def initial_setup(self):
        options = [
            ("-脅威防御ライト-", "nordvpn set threatprotectionlite on"),
            ("-キルスイッチ-", "nordvpn set killswitch on"),
            ("-自動接続-", "nordvpn set autoconnect on"),
            ("-通知-", "nordvpn set notify on"),
            ("-混乱化-", "nordvpn set obfuscate on"),
            ("-メッシュネット-", "nordvpn set meshnet on"),
        ]
        for key, command in options:
            self.window[key].update(True)  # チェックボックスをオンに設定
            result = self.run_command(command)
            print(f"{key} を設定: {result}")
            self.update_status(result)
            time.sleep(1)  # コマンド実行後少し待機

    def get_events(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == '終了':
                self.running = False  # スレッドを停止するためのフラグをセット
                break

            # 各イベントに応じた処理
            if event == "-最寄りのスタンダードサーバー-":
                print("最寄りのスタンダードサーバーに接続")
                self.update_status("最寄りのスタンダードサーバーに接続中...")
                result = self.run_command("nordvpn connect")
                self.update_status(result)
            elif event == "-P2Pサーバー-":
                print("P2Pサーバーに接続")
                self.update_status("P2Pサーバーに接続中...")
                result = self.run_command("nordvpn connect P2P")
                self.update_status(result)
            elif event == "-ダブルVPNサーバー-":
                print("ダブルVPNサーバーに接続")
                self.update_status("ダブルVPNサーバーに接続中...")
                result = self.run_command("nordvpn connect Double_VPN")
                self.update_status(result)
            elif event == "-Onion_Over_VPNサーバー-":
                print("Onion Over VPNサーバーに接続")
                self.update_status("Onion Over VPNサーバーに接続中...")
                result = self.run_command("nordvpn connect Onion_Over_VPN")
                self.update_status(result)
            elif event == "-Dedicated_IPサーバー-":
                print("Dedicated IPサーバーに接続")
                self.update_status("Dedicated IPサーバーに接続中...")
                result = self.run_command("nordvpn connect Dedicated_IP")
                self.update_status(result)
            elif event == "-Obfuscatedサーバー-":
                print("Obfuscatedサーバーに接続")
                self.update_status("Obfuscatedサーバーに接続中...")
                result = self.run_command("nordvpn connect Obfuscated")
                self.update_status(result)
            elif event == "-ログイン-":
                print("ログイン")
                self.update_status("ログイン中...")
                result = self.run_command("nordvpn login")
                self.update_status(result)
            elif event == "-切断-":
                print("VPN切断")
                self.update_status("VPN切断中...")
                result = self.run_command("nordvpn disconnect")
                self.update_status(result)
            elif event == "-ログアウト-":
                print("ログアウト")
                self.update_status("ログアウト中...")
                result = self.run_command("nordvpn logout")
                self.update_status(result)

            # その他のオプションのイベント
            elif event == "-脅威防御ライト-":
                print("脅威防御ライト", values[event])
                self.update_status("脅威防御ライトを設定中...")
                result = self.run_command(f"nordvpn set threatprotectionlite {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-キルスイッチ-":
                print("キルスイッチ", values[event])
                self.update_status("キルスイッチを設定中...")
                result = self.run_command(f"nordvpn set killswitch {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-自動接続-":
                print("自動接続", values[event])
                self.update_status("自動接続を設定中...")
                result = self.run_command(f"nordvpn set autoconnect {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-通知-":
                print("通知", values[event])
                self.update_status("通知を設定中...")
                result = self.run_command(f"nordvpn set notify {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-混乱化-":
                print("混乱化", values[event])
                self.update_status("混乱化を設定中...")
                result = self.run_command(f"nordvpn set obfuscate {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-メッシュネット-":
                print("メッシュネット", values[event])
                self.update_status("メッシュネットを設定中...")
                result = self.run_command(f"nordvpn set meshnet {'on' if values[event] else 'off'}")
                self.update_status(result)

            # 設定タブのイベント
            elif event == "systemctl_enable":
                self.update_status("systemctl enable nordvpnd 実行中...")
                result = self.run_command("sudo systemctl enable nordvpnd")
                self.update_status(result)
            elif event == "systemctl_start":
                self.update_status("systemctl start nordvpnd 実行中...")
                result = self.run_command("sudo systemctl start nordvpnd")
                self.update_status(result)
            elif event == "systemctl_stop":
                self.update_status("systemctl stop nordvpnd 実行中...")
                result = self.run_command("sudo systemctl stop nordvpnd")
                self.update_status(result)
            elif event == "systemctl_disable":
                self.update_status("systemctl disable nordvpnd 実行中...")
                result = self.run_command("sudo systemctl disable nordvpnd")
                self.update_status(result)
            elif event == "systemctl_status":
                self.update_status("systemctl status nordvpnd 実行中...")
                result = self.run_command("sudo systemctl status nordvpnd")
                self.update_status(result)
            elif event == "systemctl_restart":
                self.update_status("systemctl restart nordvpnd 実行中...")
                result = self.run_command("sudo systemctl restart nordvpnd")
                self.update_status(result)
            elif event == "ポートの開放":
                self.update_status("ポートの開放中...")
                result = self.run_command(f"sudo ufw allow {values['port_add']}")
                self.update_status(result)
            elif event == "ポートを閉じる":
                self.update_status("ポートを閉じる中...")
                result = self.run_command(f"sudo ufw deny {values['port_remove']}")
                self.update_status(result)

    def run(self):
        # スレッドを作成して開始
        event_thread = threading.Thread(target=self.get_events)
        event_thread.start()

        # スレッドが停止するまで待機
        while self.running:
            time.sleep(1)

        # スレッドが終了するのを待つ
        event_thread.join()

# GUIのインスタンスを作成して実行
gui = GUI()
gui.run()