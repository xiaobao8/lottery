# lottery
# 抽奖API

## 根据config/config.ini 修改mysql和redis的配置，还有策略的配置，并添加相应的奖品等级数据到raffle_prize表中。
## 现在写了两种策略：
  #### 策略1：
    plan=1
    会有一定概率未抽中的情况（再剩余数量极少的情况下）  但效率高  利用django的查询修改原子操作保证不超发的情况。
  #### 策略2：
    plan=2
    保证100%中奖 但并发受限  因为考虑到100%中奖 所以使用悲观锁。
    
    
## /api/raffle/send/  接口为抽奖接口。

## /api/raffle/ 可以对抽奖表增删改查。

## 启动测试代码
  #### gunicorn -w 5 --threads 3 -b 0.0.0.0:8000 --timeout 60 lottery.wsgi:application
