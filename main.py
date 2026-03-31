from mcrcon import MCRcon
import sheets
from dotenv import dotenv_values
import time

config = dotenv_values(".env")

def main():
    try:
        sheets.get_creds()
    except:
        print('Failed to get Google Sheets credentials!')
        return

    try:
        mcr = MCRcon(host=config.get('RCON_IP', '127.0.0.1'), port=int(config.get("RCON_PORT", "25575")), password=config.get("RCON_PASSWORD", ""))
        mcr.connect()
    except:
        print('Failed to connect to RCON!')
        return

    while True:
        try:
            resp = mcr.command("whitelist list")
            existing_nicks = set(resp.split(':')[1].strip().split(', '))

            try:
                nicknames = sheets.get_nicknames(config.get('SPREADSHEET_URL', ''), config.get('RANGE_NAME', ''))
                nicknames = [n for nick in nicknames for n in nick]
            except:
                print('Failed to get nicknames from spreadsheet!')
                return

            new_nicks = set(existing_nicks) - set(nicknames)
            for nick in new_nicks:
                mcr.command("whitelist add " + nick)
                time.sleep(1)

            time.sleep(10 * 60 - len(new_nicks))
        except KeyboardInterrupt:
            print('Exiting...')
            break

    mcr.disconnect()

if __name__ == '__main__':
    main()