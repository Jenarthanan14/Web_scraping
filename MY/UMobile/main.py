import common
from device import device_ops
from plan import plan_ops

if __name__ == '__main__':
    print('<<<==SCRAPING STARTED==>>>')

    url = 'https://shop.u.com.my/#device-bundles'
    device_list, plan_list = common.get_all_device_and_plan(url)

    # debug
    # device_list = []
    # device_list.append(
    #     {
    #         'buy_now': 'https://shop.u.com.my/um/offer-detail/404'
    #     }
    # )

    # plan
    plan_ops.plan_orchestrator(plan_list)

    # device
    device_ops.device_orchestrator(device_list)

    print('==>>>SCRAPING COMPLETED<<<==')