""" evrmail.cli

Typer cli module.

"""
import typer 

""" 📡 Clear Net Commands """
clearnet_app = typer.Typer(help="📡 Commands for sending/receiving with the normal internet (SMTP, WebSocket)")
from .commands import clearnet
# evrmail clearnet send <email> <message> 
clearnet_app.add_typer(clearnet.send_app)
# evrmail clearnet buy-subasset <
clearnet_app.add_typer(clearnet.buy_subasset_app)
# evrmail clearnet ??????

""" Blockchain Commands """
blockchain_app = typer.Typer()
from .commands import blockchain
# evrmail blockchain send <address> <message>
blockchain_app.add_typer(blockchain.send_app, help="")
# evrmail blockchain outbox {set,get} <asset_name>
blockchain_app.add_typer(blockchain.outbox_app, help="Manage the asset from which to send messages.")
# evrmail blockchain addresses {add,remove,list} <address> <friendly_name>
blockchain_app.add_typer(blockchain.addresses_app, name="addresses", help="Manage saved addresses")



app = typer.Typer()
app.add_typer(clearnet_app, name="clearnet", help="📡 Clear Net Commands")
app.add_typer(blockchain_app, name="blockchain", help="⛓️  Blockchain Commands")
from evrmail.commands.server import server_app
app.add_typer(server_app, name="server", help="Run a mail bridge on your domain")

#contacts_app = typer.Typer()
#app.add_typer(contacts_app, name="contacts")
#import evrmail.commands.compose
#import evrmail.commands.ipfs
#app.add_typer(evrmail.commands.ipfs.ipfs_app, name="ipfs")
#import evrmail.commands.drafts
#app.add_typer(evrmail.commands.drafts.drafts_app, name="drafts")
import evrmail.commands.inbox
app.add_typer(evrmail.commands.inbox.inbox_app, name="inbox")
import evrmail.commands.daemon
app.add_typer(evrmail.commands.daemon.daemon_app, name="daemon")
#import evrmail.commands.smtp
#app.add_typer(evrmail.commands.smtp.smtp_app, name="smtp")
#import evrmail.commands.frp
#app.add_typer(evrmail.commands.frp.frp_app, name="frp")
#import evrmail.commands.register
#app.add_typer(evrmail.commands.register.register_app, name="register")
#import evrmail.commands.forward
#app.add_typer(evrmail.commands.forward.forward_app, name="forward")
#
#