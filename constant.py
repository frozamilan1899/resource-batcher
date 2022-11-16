
# 老版资源服务，dev环境
old_srv_dev = "http://3.82.172.202:8060/resource/"
# 老版资源服务，prod环境
old_srv_prod = "https://resource-prod-minestory.minestudio.us/resource/"
# 新版资源服务，dev环境
new_srv_dev = "http://3.91.94.157:8060/resource/"
# 新版资源服务，test环境
new_srv_test = "https://resource-test.minestudio.us/resource/"
# 新版资源服务，prod环境
new_srv_prod = "https://resource-prod.minestudio.us/resource/"

# 服务器名称数组
srv_names = ["老版资源服务dev环境", "老版资源服务prod环境", "新版资源服务dev环境", "新版资源服务test环境", "新版资源服务prod环境"]
# 服务器地址数组
srv_base_urls = [old_srv_dev, old_srv_prod, new_srv_dev, new_srv_test, new_srv_prod]
srv_env_dic = dict(zip(srv_names, srv_base_urls))


# 资源类型数组
res_types = ["scene", "character", "objects", "cloth", "action", "motion", "emotion"]


# 文件类型名
res_file_types = ["preview", "minestory-win-bundle", "minestory-universal-art", "universal-universal-floor-plan", "默认类型"]