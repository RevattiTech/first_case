from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from src.button import button_start
from src.service import Service

route = Router()
service = Service()

@route.message(Command("start"))
async def start(message: Message):
    await message.answer("""
Привет, ребята из SecurityHackaton!

Рады видеть вас на нашем проекте! 🚀 Ваша работа по обеспечению безопасности просто на высоте, и мы уверены, что с вами всегда можно быть уверенными в надежности наших систем.

Если у вас есть какие-то вопросы или идеи по улучшению, не стесняйтесь обращаться. Вместе мы сможем достичь невероятных высот! 💻    
    """, reply_markup=button_start())


@route.callback_query(lambda call: call.data.startswith("req_"))
async def history(call: types.CallbackQuery) -> None:
    data = call.data.split("_")[-1]
    res = await service.exp_or_poc(data)

    if "error" in res:
        await call.message.answer(f"❌ Error: {res['error']}")
        return

    # Форматируем вывод с эмодзи и детальными данными
    formatted_message = "📜 *Exploit / PoC Details*\n\n"

    for exploit in res:
        # formatted_message += f"🔗 *Title*: [{exploit.get('name')}]({exploit.get('href')})\n"
        formatted_message += f"📄 *Title*: {exploit.get('title')}\n"
        formatted_message += f"📅 *Published*: {exploit.get('published')}\n"
        formatted_message += f"💡 *Score*: {exploit.get('score')}\n"
        formatted_message += f"🌐 *Link*: {exploit.get('href')}\n"
        formatted_message += f"----------------------------\n"
        # formatted_message += f"💾 *ID*: {exploit.get('id')}\n\n"

    # Отправляем красиво отформатированное сообщение
    await call.message.answer(formatted_message)


@route.callback_query(lambda call: call.data.startswith("history"))
async def history(call: types.CallbackQuery) -> None:
    res = await service.history(call.message.chat.id)

    formatted_message = "📊 *Here are your vulnerability scan results:* \n\n"

    for entry in res:
        formatted_message += f"🔍 **Host:** {entry['host']}\n"
        formatted_message += f"🛡️ **Status:** {entry['status']}\n"
        formatted_message += f"⏱️ **Execution Time:** {entry['execution_time']} seconds\n"
        formatted_message += f"🌐 **Open Ports:** {entry['open_port']}\n"

        if entry['vulnerabilities']:
            formatted_message += f"⚠️ **Vulnerabilities:**\n"
            for vuln in entry['vulnerabilities']:
                formatted_message += f"🚨 **Vulnerability:** {vuln['vulnerability']}\n"
                formatted_message += f"  📝 **Description:** {vuln['description']}\n"
                formatted_message += f"  💥 **Exploit:** {vuln['exploit']}\n"
                formatted_message += f"  🔌 **Port:** {vuln['port']}\n"
                formatted_message += f"  ✅ **Recommendation:** {vuln['recommendation']}\n"
                formatted_message += "\n"
        else:
            formatted_message += "✔️ **No vulnerabilities found.**\n"

        formatted_message += "---------------------------------\n \n"

    await call.message.answer(formatted_message)


class ScanTg(StatesGroup):
    ip = State()


@route.callback_query(lambda call: call.data.startswith("scan"))
async def search(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Please enter an IP address or domain name:")
    await state.set_state(ScanTg.ip)



@route.message(ScanTg.ip)
async def search_req(message: types.Message, state: FSMContext) -> None:
    ip_or_domain = message.text

    try:
        result = await service.scan(ip_or_domain, message.chat.id)

        if "error" in result:
            await message.answer(f"❌ Error: {result['error']}", parse_mode=ParseMode.MARKDOWN)
        else:
            vulnerabilities_details = ""
            for vuln in result.get("vulnerabilities", []):
                vulnerabilities_details += (
                    f"\n🔴 Vulnerability: {vuln['vulnerability']} (Port: {vuln['port']})\n"
                    f"  📜 Description: {vuln['description']}\n"
                    f"  💡 Recommendation: {vuln['recommendation']}\n"
                    f"  ⚡ Exploit: {vuln['exploit']}\n"
                )

            await message.answer(
                f"✅ **Scan completed successfully!**\n\n"
                f"🌐 **Host:** {result.get('url')}\n"
                f"🔓 **Open Ports:** {', '.join(map(str, result.get('open_ports', [])))}\n"
                f"⚠️ **Vulnerabilities Found:** {len(result.get('vulnerabilities', []))}\n"
                f"🛡️ **Status:** {result.get('status')}\n"
                f"⏱️ **Execution Time:** {result.get('execution_time')} seconds\n"
                f"{vulnerabilities_details if vulnerabilities_details else 'No vulnerabilities found.'}",
                parse_mode=ParseMode.MARKDOWN
            )

            await state.clear()
    except Exception as e:
        await message.answer(f"❌ Something went wrong: {str(e)}", parse_mode=ParseMode.MARKDOWN)
