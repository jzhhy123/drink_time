# 喝水时间 → iOS App（TestFlight）操作清单

你是 **Windows + iPhone，无 Mac**。路线：Capacitor 工程 → Codemagic 云端 Mac 编译签名 → TestFlight 给几个人试用。
代码部分我已做完。下面 ❗ 标记的是**只能你本人做**的账号操作，按顺序来。

---

## 已完成（无需你操作）
- `www/index.html`：完整 App（喝水/记录/取数/设置 四页，水滴动画、备注+图片、苹果式日历圆环）
- 接入 **Capacitor 原生本地通知**：App 关闭时每小时也能弹「今日饮水目标尚未达成，记得喝水」
  - 实现方式：一次预排 60 条未来通知，每次打开 App 自动重排（iOS 单 App 待发通知上限 64，够用）
- `package.json` / `capacitor.config.json` / `codemagic.yaml` / `.gitignore` 均已配好并验证

> 本地预览：直接双击 `www/index.html` 即可看界面（通知会走网页弹窗，原生通知只在真机 App 内生效）。

---

## ❗ 第 1 步：注册 Apple 开发者账号（99 美元/年）
1. 打开 https://developer.apple.com/programs/ → Enroll
2. 用你的 Apple ID 登录，按个人(Individual)注册，付 99 美元
3. 审核通过通常几小时~2 天。**没通过前后续步骤做不了**

## ❗ 第 2 步：App Store Connect 建 App
1. 打开 https://appstoreconnect.apple.com → 我的 App → ＋ → 新建 App
2. 平台 iOS；名称随意（如「喝水时间」）；主语言中文
3. 套装 ID（Bundle ID）：选「注册新的」，填 `com.drinktime.app`
   - 想用别的 ID 也行，但要全球唯一；改了的话**告诉我**，我同步改 2 个配置文件
4. SKU 随便填（如 `drinktime001`）
5. 建好后进入该 App，地址栏里那串数字就是 **Apple ID（10 位数字）**，记下来

## ❗ 第 3 步：生成 App Store Connect API 密钥
1. App Store Connect → 用户和访问 → 集成/密钥 → App Store Connect API
2. 生成密钥，角色选 **App Manager**（要能创建签名）
3. 记下 **Issuer ID**、**Key ID**，并下载 `.p8` 文件（只能下一次，保存好）

## ❗ 第 4 步：把代码推到 GitHub
1. 注册/登录 https://github.com ，新建一个空仓库（Private 即可），名字如 `drink-time`
2. 在本机 `D:\AI\Drink Time` 目录打开 PowerShell，依次执行（把 URL 换成你的仓库）：
   ```
   git init
   git add .
   git commit -m "喝水时间 Capacitor 工程"
   git branch -M main
   git remote add origin https://github.com/你的用户名/drink-time.git
   git push -u origin main
   ```
   > 需要我帮你执行这步可以直接说。

## ❗ 第 5 步：Codemagic 配置并构建
1. 打开 https://codemagic.io ，用 GitHub 账号登录（有免费额度，够用）
2. Add application → 选刚才的 `drink-time` 仓库 → 选 **codemagic.yaml** 模式
3. 左侧 Teams → Integrations → **App Store Connect** → Add key：
   - 名称必须填 **`CodemagicASC`**（和 codemagic.yaml 里一致）
   - 上传第 3 步的 `.p8`，填 Issuer ID、Key ID
4. 打开 `codemagic.yaml`，把 `APP_STORE_APPLE_ID: 0000000000` 改成第 2 步记下的数字
   - 改完重新 `git add . && git commit -m "set apple id" && git push`
5. 回 Codemagic → Start new build → 选 `ios-testflight` workflow → 开始
   - 首次约 10~20 分钟。成功后 IPA 会自动上传到 TestFlight

## ❗ 第 6 步：TestFlight 邀请试用者
1. App Store Connect → 你的 App → TestFlight 标签
2. 构建处理完（几分钟，会从「正在处理」变可用）
3. 内部测试（最快，最多 100 人，需是你团队成员）：直接加测试员邮箱
   外部测试：建测试组、加邮箱，**首次需 Apple 简单 Beta 审核**（1~2 天）
4. 试用者在 iPhone 装「TestFlight」App，点邀请邮件/链接接受 → 装上你的 App

---

## 费用与时间预估
| 项 | 费用 | 时间 |
|---|---|---|
| Apple 开发者账号 | 99 美元/年 | 审核数小时~2 天 |
| Codemagic | 免费额度足够个人/小范围 | 每次构建 10~20 分钟 |
| 外部 TestFlight 首次审核 | 免费 | 1~2 天 |

## 卡住了怎么办
任何一步报错，把**报错截图或文字**发我，我帮你定位。
改 Bundle ID、改 App 名、调界面或加功能，也随时说。
