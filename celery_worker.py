from app import create_app
from extensions import cel_app  # Don't del!!

# 让当前进程初始化flask组件
app = create_app(activate_mq=False)
