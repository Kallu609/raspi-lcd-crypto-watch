from .add_crypto import AddCrypto
from .remove_crypto import RemoveCrypto
from .show_watchlist import ShowWatchlist
from .limit import Limit

commands = [
    # [[identifier(s)], class, pass_args]
    [['add'], AddCrypto, True],
    [['remove', 'del'], RemoveCrypto, True],
    [['watchlist', 'wl'], ShowWatchlist, False],
    [['addlimit', 'limits', 'limit', 'notify'], Limit, True]
]
