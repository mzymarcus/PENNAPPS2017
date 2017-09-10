from oslo_config import cfg

opts = [
    cfg.IntOpt(
        "port",
        default=50008,
    ),
]

cfg.CONF.register_cli_opts(opts)