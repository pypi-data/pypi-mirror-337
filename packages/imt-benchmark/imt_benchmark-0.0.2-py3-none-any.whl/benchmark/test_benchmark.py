import benchmark


def test_data_available():
    imtp = benchmark.IMTP(["seg1"])
    _ = benchmark.benchmark(imtp, 1, "slow1")
    _ = imtp.sys(1)
