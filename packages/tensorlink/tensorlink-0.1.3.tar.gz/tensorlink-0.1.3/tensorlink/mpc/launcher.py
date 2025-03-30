from tensorlink.mpc.nodes import UserNode


def create_user_node():
    return UserNode(upnp=True, off_chain_test=False, local_test=False)
