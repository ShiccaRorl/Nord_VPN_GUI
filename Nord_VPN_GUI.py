import PySimpleGUI as sg
import subprocess
import threading
import time

class GUI:
    def __init__(self):
        self.window = sg.Window("Nord_VPN_GUI", self.get_layout(), resizable=True, finalize=True)
        self.running = True
        self.init_system = self.check_init_system()

    def get_layout(self):
        接続タブ = [
            [sg.Text("Nord VPN", size=(15, 1))],
            [sg.Button("最寄りのスタンダードサーバー", key="-最寄りのスタンダードサーバー-")],
            [sg.Button("P2Pサーバー", key="-P2Pサーバー-")],
            [sg.Button("ダブルVPNサーバー", key="-ダブルVPNサーバー-")],
            [sg.Button("Onion Over VPNサーバー", key="-Onion_Over_VPNサーバー-")],
            [sg.Button("Dedicated IPサーバー", key="-Dedicated_IPサーバー-")],
            [sg.Button("Obfuscatedサーバー", key="-Obfuscatedサーバー-")],
            [sg.Button("ログイン", key="-ログイン-"), sg.Button("切断", key="-切断-"), sg.Button("ログアウト", key="-ログアウト-")]
        ]

        オプションタブ = [
            [sg.Text("オプション")],
            [sg.Checkbox("脅威防御ライト", True, key="-脅威防御ライト-")],
            [sg.Checkbox("キルスイッチ", True, key="-キルスイッチ-")],
            [sg.Checkbox("自動接続", True, key="-自動接続-")],
            [sg.Checkbox("通知", True, key="-通知-")],
            [sg.Checkbox("混乱化", True, key="-混乱化-")],
            [sg.Checkbox("メッシュネット", True, key="-メッシュネット-")],
            [sg.Button("全部設定")],
            [sg.Button("全ての設定をオフにする", key="-RESET_SETTINGS-")],
        ]

        ステータス = [
            [sg.Text("ステータス")],
            [sg.Text("", key="-ステータス-", size=(60, 1))]
        ]

        設定タブ = [
            [sg.Text("設定")],
            [sg.Button("インストール", key='-インストール-', size=(50, 1))],
            [sg.Button("systemctl enable nordvpnd", key="systemctl_enable")],
            [sg.Button("systemctl start nordvpnd", key="systemctl_start")],
            [sg.Button("systemctl stop nordvpnd", key="systemctl_stop")],
            [sg.Button("systemctl disable nordvpnd", key="systemctl_disable")],
            [sg.Button("systemctl status nordvpnd", key="systemctl_status")],
            [sg.Button("systemctl restart nordvpnd", key="systemctl_restart")],
            [sg.Input("", key="port_add"), sg.Button("ポートの開放")],
            [sg.Input("", key="port_remove"), sg.Button("ポートを閉じる")]
        ]

        tab_group = sg.TabGroup([
            [sg.Tab('接続', 接続タブ), sg.Tab('オプション', オプションタブ), sg.Tab('設定', 設定タブ)]
        ])

        layout = [
            [tab_group],
            [sg.Column(ステータス)]
        ]

        return layout

    def run_command(self, command):
        try:
            print(f"Running command: {command}")  # デバッグ出力
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            print(f"Command result: {result.stdout if result.returncode == 0 else result.stderr}")  # デバッグ出力
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            print(f"Command error: {e}")  # デバッグ出力
            return str(e)

    def check_init_system(self):
        try:
            with open('/proc/1/comm', 'r') as f:
                init_system = f.read().strip()
            return init_system
        except Exception as e:
            return str(e)

    def update_status(self, message):
        self.window['-ステータス-'].update(message)

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
            self.window[key].update(True)
            result = self.run_command(command)
            print(f"{key} を設定: {result}")
            self.update_status(f"{key} を設定: {result}")
            time.sleep(1)

    def get_events(self):
        while self.running:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == '終了':
                self.running = False
                break

            if event.startswith('-'):
                self.update_status(f"Event: {event}")

            # 各イベントに応じた処理
            elif event == "-最寄りのスタンダードサーバー-":
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
                # URLを抽出して表示
                url_start = result.find('https://')
                if url_start != -1:
                    url_end = result.find(' ', url_start)
                    url = result[url_start:url_end].strip()
                    self.window['-ログインURL-'].update(url)
                    self.update_status(f"ブラウザでログインを完了してください: {url}")
                else:
                    self.update_status("ログインURLを取得できませんでした。")
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
            elif event == "-コピー-":
                # ログインURLをクリップボードにコピー
                url = values['-ログインURL-']
                sg.clipboard_set(url)
                self.update_status("ログインURLをクリップボードにコピーしました")

            elif event == "-脅威防御ライト-":
                print("脅威防御ライトを設定中...")
                self.update_status("脅威防御ライトを設定中...")
                result = self.run_command(f"nordvpn set threatprotectionlite {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-キルスイッチ-":
                print("キルスイッチを設定中...")
                self.update_status("キルスイッチを設定中...")
                result = self.run_command(f"nordvpn set killswitch {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-自動接続-":
                print("自動接続を設定中...")
                self.update_status("自動接続を設定中...")
                result = self.run_command(f"nordvpn set autoconnect {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-通知-":
                print("通知を設定中...")
                self.update_status("通知を設定中...")
                result = self.run_command(f"nordvpn set notify {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-混乱化-":
                print("混乱化を設定中...")
                self.update_status("混乱化を設定中...")
                result = self.run_command(f"nordvpn set obfuscate {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "-メッシュネット-":
                print("メッシュネットを設定中...")
                self.update_status("メッシュネットを設定中...")
                result = self.run_command(f"nordvpn set meshnet {'on' if values[event] else 'off'}")
                self.update_status(result)
            elif event == "全部設定":
                print("設定中...")
                self.update_status("設定中...")
                options = [
                    ("-脅威防御ライト-", "nordvpn set threatprotectionlite"),
                    ("-キルスイッチ-", "nordvpn set killswitch"),
                    ("-自動接続-", "nordvpn set autoconnect"),
                    ("-通知-", "nordvpn set notify"),
                    ("-混乱化-", "nordvpn set obfuscate"),
                    ("-メッシュネット-", "nordvpn set meshnet"),
                ]
                for key, command in options:
                    state = 'on' if values[key] else 'off'
                    result = self.run_command(f"{command} {state}")
                    self.update_status(result)
                    time.sleep(1)

            elif event == "-RESET_SETTINGS-":
                print("全ての設定をオフにする")
                self.update_status("全ての設定をオフにしています...")
                commands = [
                    "nordvpn set autoconnect off",
                    "nordvpn set killswitch off",
                    "nordvpn set threatprotectionlite off",
                    "nordvpn set notify off",
                    "nordvpn set obfuscate off",
                    "nordvpn set meshnet off"
                ]
                for command in commands:
                    result = self.run_command(command)
                    self.update_status(result)
                    time.sleep(1)

            # 設定タブのイベント
            elif event == "systemctl_enable":
                self.update_status("systemctl enable nordvpnd 実行中...")
                result = self.run_command("systemctl enable nordvpnd")
                self.update_status(result)
            elif event == "systemctl_start":
                self.update_status("systemctl start nordvpnd 実行中...")
                result = self.run_command("systemctl start nordvpnd")
                self.update_status(result)
            elif event == "systemctl_stop":
                self.update_status("systemctl stop nordvpnd 実行中...")
                result = self.run_command("systemctl stop nordvpnd")
                self.update_status(result)
            elif event == "systemctl_disable":
                self.update_status("systemctl disable nordvpnd 実行中...")
                result = self.run_command("systemctl disable nordvpnd")
                self.update_status(result)
            elif event == "systemctl_status":
                if self.init_system == 'systemd':
                    result = self.run_command("systemctl status nordvpnd")
                elif self.init_system == 'init':
                    result = self.run_command("service nordvpnd status")
                else:
                    result = "Unsupported init system: {}".format(self.init_system)
                self.update_status(result)        
            elif event == "systemctl_restart":
                self.update_status("systemctl restart nordvpnd 実行中...")
                result = self.run_command("systemctl restart nordvpnd")
                self.update_status(result)
            elif event == "ポートの開放":
                port = values["port_add"]
                self.update_status(f"ポート {port} を開放中...")
                result = self.run_command(f"ufw allow {port}")
                self.update_status(result)
            elif event == "ポートを閉じる":
                port = values["port_remove"]
                self.update_status(f"ポート {port} を閉じる中...")
                result = self.run_command(f"ufw deny {port}")
                self.update_status(result)

if __name__ == "__main__":
    gui = GUI()
    #threading.Thread(target=gui.initial_setup).start()
    gui.get_events()
