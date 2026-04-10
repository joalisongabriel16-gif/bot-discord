import os
import asyncio
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

GUILD_ID = 1473566201568428042
CANAL_PAINEL_ID = 1473583190026227862
CANAL_APROVACAO_ID = 1491940609471021116
CATEGORIA_FORMULARIOS_ID = 1473566202025611385
CARGO_APROVADO_ID = 1491953202780836111

# Logo pequena
LOGO_URL = "https://cdn.discordapp.com/attachments/1206797344540987496/1491990878657576970/image.png"

# Imagem grande da pergunta 5
PERGUNTA5_IMAGEM_URL = "https://cdn.discordapp.com/attachments/1206797344540987496/1491988986116309112/image.png"

# Banner grande do embed inicial
BANNER_INICIO_URL = "https://cdn.discordapp.com/attachments/1206797344540987496/1491990978100199525/Atraia_poder_torne-se_staff_1.png"

# Imagem da última embed de finalização
IMAGEM_FINAL_URL = "https://cdn.discordapp.com/attachments/1206797344540987496/1491996706349256896/Mafia_e_misterio_no_horizonte.png"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

formularios_ativos = {}

PERGUNTAS = [
    ("1. Nome", "Nome:", "texto"),
    ("2. Idade", "Idade:", "texto"),
    ("3. Quanto tempo você joga RP", "Quanto tempo você joga RP:", "texto"),
    ("4. Disponibilidade", "Disponibilidade:", "select"),
    ("5. Seu ID do Discord", "Seu ID do Discord: (Ex: Imagem abaixo)", "texto"),
    ("6. Já teve alguma experiência com Staff?", "Já teve alguma experiência com Staff?", "simnao"),
    ("7. Dê o significado de DARK RP", "Dê o significado de DARK RP:", "texto"),
    ("8. Dê o significado de RDM", "Dê o significado de RDM:", "texto"),
    ("9. Dê o significado de VDM", "Dê o significado de VDM:", "texto"),
    ("10. Dê o significado de COMBAT LOGGIN", "Dê o significado de COMBAT LOGGIN:", "texto"),
    ("11. Dê o significado de AMOR À VIDA", "Dê o significado de AMOR À VIDA:", "texto"),
    ("12. Dê o significado de POWER GAMING", "Dê o significado de POWER GAMING:", "texto"),
    ("13. Dê o significado de META GAMING", "Dê o significado de META GAMING:", "texto"),
    ("14. Cite 4 regras da cidade", "Cite 4 regras da cidade:", "texto"),
    (
        "15. Situação de sequestro",
        "Suponhamos que você foi sequestrado e durante o sequestro você percebe que o bandido está altamente agressivo com você, você em posição de refém o que faria?",
        "texto"
    ),
    (
        "16. Situação de VIP ilegal",
        "Suponhamos que você está randolando na praça e uma pessoa chega pra você falando que vende VIP em troca de dinheiro na cidade, o que você faria?",
        "texto"
    ),
    ("17. Cite seus defeitos e suas qualidades", "Cite seus defeitos e suas qualidades:", "texto"),
    ("18. Explique para mim o que é maturidade", "Explique para mim o que é maturidade:", "texto"),
    (
        "19. Me fale um pouco sobre você e por que deveríamos te aprovar em nossa Staff",
        "Me fale um pouco sobre você e por que deveríamos te aprovar em nossa Staff:",
        "texto"
    ),
    (
        "20. Ciente sobre programas ilegais e abuso de privilégios",
        "Você está ciente de que, ao identificarmos que você esteja utilizando algum programa ILEGAL ou até mesmo usando seus privilégios de staff para benefício próprio, você estará sujeito a BANIMENTO PERMANENTE da equipe e da cidade?",
        "ciente"
    ),
    (
        "21. Ciente sobre sigilo da staff",
        "Você está ciente de que, ao entrar na staff, todas as informações obtidas deverão ser mantidas em total sigilo e, caso você quebre essa regra, estará sujeito a banimento permanente da equipe?",
        "ciente"
    ),
    (
        "22. Ciente sobre a Lei nº 15.211/2025 - ECA Digital",
        "Você está ciente de que a Lei nº 15.211/2025, conhecida como “ECA Digital”, entrou em vigor em 17 de março de 2026 com o objetivo de proteger menores de 18 anos na internet, exigindo verificação rigorosa de idade e restringindo conteúdos sexualizados ou adultos em redes sociais e jogos?",
        "ciente"
    ),
    (
        "23. Declaração final",
        "Declaro que estou ciente e concordo com todas as regras da staff, comprometendo-me a agir com responsabilidade, ética e imparcialidade, mantendo sigilo sobre informações internas e respeitando as diretrizes estabelecidas. Estou ciente também de que minha participação na staff não possui qualquer vínculo empregatício, sendo uma atividade voluntária, e que o descumprimento das regras poderá resultar em punições, incluindo banimento permanente.",
        "ciente"
    ),
]


def criar_embed_padrao(titulo, descricao, cor=discord.Color.blurple()):
    embed = discord.Embed(
        title=titulo,
        description=descricao,
        color=cor
    )

    if LOGO_URL:
        embed.set_thumbnail(url=LOGO_URL)

    return embed


def embed_pergunta(n, total, texto, tipo):
    embed = discord.Embed(
        title=f"📋 Pergunta {n}/{total}",
        color=discord.Color.blue()
    )

    if not texto:
        texto = "Pergunta não definida."

    if tipo == "select":
        valor_pergunta = f"{texto}\n\nOpções:\n• Manhã\n• Tarde\n• Noite\n• Madrugada"
    elif tipo == "simnao":
        valor_pergunta = f"{texto}\n\nResponda usando os botões abaixo."
    elif tipo == "ciente":
        valor_pergunta = f"{texto}\n\nClique em **Estou ciente!** para continuar."
    else:
        valor_pergunta = texto

    embed.add_field(
        name="Pergunta",
        value=valor_pergunta,
        inline=False
    )

    embed.add_field(
        name="Progresso",
        value=f"{n}/{total}",
        inline=True
    )

    embed.add_field(
        name="Tempo para responder",
        value="5 minutos",
        inline=True
    )

    embed.set_footer(
        text="Caso passe de 5 minutos, o formulário será cancelado automaticamente."
    )

    if LOGO_URL:
        embed.set_thumbnail(url=LOGO_URL)

    if n == 5 and PERGUNTA5_IMAGEM_URL:
        embed.set_image(url=PERGUNTA5_IMAGEM_URL)

    return embed


def formatar_respostas(respostas):
    texto = ""
    i = 1

    for pergunta, resposta in respostas.items():
        bloco = f"**{i}. {pergunta}**\n{resposta}\n----------------------------------\n"
        if len(texto) + len(bloco) > 4000:
            break
        texto += bloco
        i += 1

    return texto


async def perguntar_texto(canal, user, pergunta, n, total):
    msg_embed = await canal.send(embed=embed_pergunta(n, total, pergunta, "texto"))

    def check(m):
        return m.author == user and m.channel == canal

    try:
        msg = await bot.wait_for("message", check=check, timeout=300)
    except asyncio.TimeoutError:
        try:
            await msg_embed.delete()
        except:
            pass
        raise TimeoutError

    try:
        await msg.delete()
    except:
        pass

    try:
        await msg_embed.delete()
    except:
        pass

    if msg.content.lower() == "cancelar":
        raise TimeoutError

    return msg.content


class DisponibilidadeSelect(discord.ui.Select):
    def __init__(self, user, future):
        self.user = user
        self.future = future

        options = [
            discord.SelectOption(label="Manhã", emoji="🌅", value="Manhã"),
            discord.SelectOption(label="Tarde", emoji="☀️", value="Tarde"),
            discord.SelectOption(label="Noite", emoji="🌙", value="Noite"),
            discord.SelectOption(label="Madrugada", emoji="🌌", value="Madrugada"),
        ]

        super().__init__(
            placeholder="Escolha sua disponibilidade",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message(
                "Você não pode usar este formulário.",
                ephemeral=True
            )
            return

        if not self.future.done():
            self.future.set_result(self.values[0])

        await interaction.response.defer()

        try:
            await interaction.message.delete()
        except:
            pass


class SelectView(discord.ui.View):
    def __init__(self, user, future):
        super().__init__(timeout=300)
        self.user = user
        self.future = future
        self.add_item(DisponibilidadeSelect(user, future))

    async def on_timeout(self):
        if not self.future.done():
            self.future.set_exception(TimeoutError())


class SimNaoView(discord.ui.View):
    def __init__(self, user, future):
        super().__init__(timeout=300)
        self.user = user
        self.future = future

    async def on_timeout(self):
        if not self.future.done():
            self.future.set_exception(TimeoutError())

    @discord.ui.button(label="Sim!", style=discord.ButtonStyle.green, emoji="✅")
    async def sim(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Você não pode usar este botão.", ephemeral=True)
            return

        if not self.future.done():
            self.future.set_result("Sim!")

        await interaction.response.defer()

        try:
            await interaction.message.delete()
        except:
            pass

    @discord.ui.button(label="Não!", style=discord.ButtonStyle.red, emoji="❌")
    async def nao(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Você não pode usar este botão.", ephemeral=True)
            return

        if not self.future.done():
            self.future.set_result("Não!")

        await interaction.response.defer()

        try:
            await interaction.message.delete()
        except:
            pass


class CienteView(discord.ui.View):
    def __init__(self, user, future):
        super().__init__(timeout=300)
        self.user = user
        self.future = future

    async def on_timeout(self):
        if not self.future.done():
            self.future.set_exception(TimeoutError())

    @discord.ui.button(label="Estou ciente!", style=discord.ButtonStyle.green, emoji="✅")
    async def ciente(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Você não pode usar este botão.", ephemeral=True)
            return

        if not self.future.done():
            self.future.set_result("Estou ciente!")

        await interaction.response.defer()

        try:
            await interaction.message.delete()
        except:
            pass


class StaffAnaliseView(discord.ui.View):
    def __init__(self, candidato: discord.Member, respostas: dict, canal_formulario: discord.TextChannel):
        super().__init__(timeout=None)
        self.candidato = candidato
        self.respostas = respostas
        self.canal_formulario = canal_formulario
        self.finalizado = False

    async def desativar_botoes(self):
        for item in self.children:
            item.disabled = True

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.green, emoji="✅")
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.finalizado:
            await interaction.response.send_message("Este formulário já foi analisado.", ephemeral=True)
            return

        self.finalizado = True
        staff = interaction.user
        cargo = interaction.guild.get_role(CARGO_APROVADO_ID)

        if cargo is not None:
            try:
                await self.candidato.add_roles(cargo, reason=f"Aprovado por {staff}")
            except:
                pass

        embed_resultado = discord.Embed(
            title="✅ Candidato aprovado",
            color=discord.Color.green()
        )
        embed_resultado.add_field(
            name="Candidato",
            value=f"{self.candidato.mention}\n`{self.candidato.id}`",
            inline=True
        )
        embed_resultado.add_field(
            name="Aprovado por",
            value=f"{staff.mention}\n`{staff.id}`",
            inline=True
        )
        embed_resultado.add_field(
            name="Cargo entregue",
            value=cargo.mention if cargo else "Cargo não encontrado",
            inline=False
        )
        embed_resultado.set_footer(text="Sistema de recrutamento staff")

        if LOGO_URL:
            embed_resultado.set_thumbnail(url=LOGO_URL)

        try:
            dm_embed = discord.Embed(
                title="✅ Resultado da sua candidatura",
                description="Parabéns! Sua candidatura para a staff foi **aprovada**.",
                color=discord.Color.green()
            )
            dm_embed.set_image(url="https://cdn.discordapp.com/attachments/1206797344540987496/1492012571316846682/Aprovado_pela_mafia_urbana.png?ex=69d9c87d&is=69d876fd&hm=97b37ed69e038617e7bc3849f38b91fb22b792e9310bd268923677e3bd239fbf&")
            dm_embed.add_field(name="Servidor", value=interaction.guild.name, inline=False)
            dm_embed.add_field(name="Responsável", value=str(staff), inline=False)
            dm_embed.set_footer(text="Bem-vindo(a) à equipe!")
            if LOGO_URL:
                dm_embed.set_thumbnail(url=LOGO_URL)
            await self.candidato.send(embed=dm_embed)
        except:
            pass

        await self.desativar_botoes()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed_resultado)

        try:
            aviso = await self.canal_formulario.send(
                embed=criar_embed_padrao(
                    "✅ Formulário encerrado",
                    "Seu formulário foi aprovado e este canal será apagado em 5 segundos.",
                    discord.Color.green()
                )
            )
            await asyncio.sleep(5)
            try:
                await aviso.delete()
            except:
                pass
            await self.canal_formulario.delete()
        except:
            pass

    @discord.ui.button(label="Reprovar", style=discord.ButtonStyle.red, emoji="❌")
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.finalizado:
            await interaction.response.send_message("Este formulário já foi analisado.", ephemeral=True)
            return

        self.finalizado = True
        staff = interaction.user

        embed_resultado = discord.Embed(
            title="❌ Candidato reprovado",
            color=discord.Color.red()
        )
        embed_resultado.add_field(
            name="Candidato",
            value=f"{self.candidato.mention}\n`{self.candidato.id}`",
            inline=True
        )
        embed_resultado.add_field(
            name="Reprovado por",
            value=f"{staff.mention}\n`{staff.id}`",
            inline=True
        )
        embed_resultado.set_footer(text="Sistema de recrutamento staff")

        if LOGO_URL:
            embed_resultado.set_thumbnail(url=LOGO_URL)

        try:
            dm_embed = discord.Embed(
                title="❌ Resultado da sua candidatura",
                description="Sua candidatura para a staff foi **reprovada**.",
                color=discord.Color.red()
            )
            dm_embed.set_image(url="https://cdn.discordapp.com/attachments/1206797344540987496/1492012570800951386/A_cena_da_ultima_sentenca.png?ex=69d9c87d&is=69d876fd&hm=c0c7b1526cda141cb6594ba4f713a48854552dac9cd0ee12cfb9e445abfae224&")
            dm_embed.add_field(name="Servidor", value=interaction.guild.name, inline=False)
            dm_embed.add_field(name="Responsável", value=str(staff), inline=False)
            dm_embed.set_footer(text="Você poderá tentar novamente futuramente, caso a cidade permita.")
            if LOGO_URL:
                dm_embed.set_thumbnail(url=LOGO_URL)
            await self.candidato.send(embed=dm_embed)
        except:
            pass

        await self.desativar_botoes()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed_resultado)

        try:
            aviso = await self.canal_formulario.send(
                embed=criar_embed_padrao(
                    "❌ Formulário encerrado",
                    "Seu formulário foi reprovado e este canal será apagado em 5 segundos.",
                    discord.Color.red()
                )
            )
            await asyncio.sleep(5)
            try:
                await aviso.delete()
            except:
                pass
            await self.canal_formulario.delete()
        except:
            pass


class FinalizarView(discord.ui.View):
    def __init__(self, user, respostas, canal):
        super().__init__(timeout=300)
        self.user = user
        self.respostas = respostas
        self.canal = canal

    @discord.ui.button(label="Finalizar", style=discord.ButtonStyle.green, emoji="📨")
    async def finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Você não pode finalizar este formulário.", ephemeral=True)
            return

        await interaction.response.defer()

        canal_staff = interaction.guild.get_channel(CANAL_APROVACAO_ID)

        if canal_staff is None:
            await self.canal.send("Não encontrei o canal de aprovação configurado.")
            return

        embed = discord.Embed(
            title="📨 Nova candidatura recebida",
            description=formatar_respostas(self.respostas),
            color=discord.Color.orange()
        )
        embed.add_field(name="Candidato", value=self.user.mention, inline=True)
        embed.add_field(name="ID", value=f"`{self.user.id}`", inline=True)
        embed.add_field(name="Tempo por pergunta", value="5 minutos", inline=True)
        embed.set_footer(text="Use os botões abaixo para aprovar ou reprovar.")

        if LOGO_URL:
            embed.set_thumbnail(url=LOGO_URL)

        view_staff = StaffAnaliseView(self.user, self.respostas, self.canal)
        await canal_staff.send(embed=embed, view=view_staff)

        try:
            dm_embed = discord.Embed(
                title="📩 Formulário enviado",
                description="Seu formulário foi enviado com sucesso para análise da equipe.",
                color=discord.Color.gold()
            )
            dm_embed.add_field(name="Tempo por pergunta", value="5 minutos", inline=False)
            dm_embed.set_footer(text="Aguarde o retorno da staff.")
            if LOGO_URL:
                dm_embed.set_thumbnail(url=LOGO_URL)
            await self.user.send(embed=dm_embed)
        except:
            pass

        try:
            await interaction.message.delete()
        except:
            pass

        await self.canal.send(
            embed=criar_embed_padrao(
                "✅ Formulário enviado",
                "Seu formulário foi enviado para análise da staff.\nAguarde o resultado em sua DM.",
                discord.Color.green()
            )
        )


async def iniciar(canal, user):
    intro = await canal.send(
        embed=criar_embed_padrao(
            "📋 Formulário iniciado",
            "Você tem **5 minutos em cada pergunta**.\nResponda tudo com atenção.\nDigite `cancelar` para encerrar o formulário.",
            discord.Color.blurple()
        )
    )

    await asyncio.sleep(5)

    try:
        await intro.delete()
    except:
        pass

    respostas = {}
    total = len(PERGUNTAS)
    n = 1

    try:
        for campo, pergunta, tipo in PERGUNTAS:
            if tipo == "texto":
                respostas[campo] = await perguntar_texto(canal, user, pergunta, n, total)

            elif tipo == "select":
                future = asyncio.get_running_loop().create_future()
                view = SelectView(user, future)
                msg = await canal.send(embed=embed_pergunta(n, total, pergunta, tipo), view=view)

                try:
                    respostas[campo] = await future
                finally:
                    try:
                        await msg.delete()
                    except:
                        pass
                    view.stop()

            elif tipo == "simnao":
                future = asyncio.get_running_loop().create_future()
                view = SimNaoView(user, future)
                msg = await canal.send(embed=embed_pergunta(n, total, pergunta, tipo), view=view)

                try:
                    respostas[campo] = await future
                finally:
                    try:
                        await msg.delete()
                    except:
                        pass
                    view.stop()

            elif tipo == "ciente":
                future = asyncio.get_running_loop().create_future()
                view = CienteView(user, future)
                msg = await canal.send(embed=embed_pergunta(n, total, pergunta, tipo), view=view)

                try:
                    respostas[campo] = await future
                finally:
                    try:
                        await msg.delete()
                    except:
                        pass
                    view.stop()

            n += 1

        embed_final = criar_embed_padrao(
            "🏁 Finalização",
            "Clique no botão abaixo para enviar seu formulário para análise.\nCada pergunta teve tempo limite de 5 minutos.",
            discord.Color.green()
        )

        if IMAGEM_FINAL_URL:
            embed_final.set_image(url=IMAGEM_FINAL_URL)

        await canal.send(
            embed=embed_final,
            view=FinalizarView(user, respostas, canal)
        )

    except TimeoutError:
        await canal.send(
            embed=criar_embed_padrao(
                "⏰ Tempo esgotado",
                "O formulário foi cancelado porque uma pergunta passou de 5 minutos sem resposta.\nEste canal será apagado em 5 segundos.",
                discord.Color.red()
            )
        )
        await asyncio.sleep(5)

        try:
            await canal.delete()
        except:
            pass

    finally:
        if user.id in formularios_ativos:
            del formularios_ativos[user.id]


class StartView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir formulário", style=discord.ButtonStyle.primary, emoji="📋")
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        if user.id in formularios_ativos:
            await interaction.response.send_message(
                "Você já possui um formulário em andamento.",
                ephemeral=True
            )
            return

        categoria = guild.get_channel(CATEGORIA_FORMULARIOS_ID)
        if categoria is None:
            await interaction.response.send_message(
                "Categoria de formulários não encontrada.",
                ephemeral=True
            )
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                manage_messages=True,
                read_message_history=True
            )
        }

        canal = await guild.create_text_channel(
            name=f"form-{user.name}".lower().replace(" ", "-"),
            category=categoria,
            overwrites=overwrites
        )

        formularios_ativos[user.id] = canal.id

        await interaction.response.send_message(
            f"Seu formulário foi criado em {canal.mention}",
            ephemeral=True
        )

        bot.loop.create_task(iniciar(canal, user))


@bot.command()
async def painelstaff(ctx):
    embed = discord.Embed(
        title="📋 Formulário Para Staff da Máfia RP📋",
        description=(
            "♛═════ 𝐑𝐞𝐪𝐮𝐢𝐬𝐢𝐭𝐨𝐬 𝐌𝐢́𝐧𝐢𝐦𝐨𝐬 ═════♛\n\n"
            "• Ter no mínimo 18 Anos de idade;\n"
            "• Ter no mínimo 1 meses de RP;\n"
            "• Ter responsabilidade e maturidade;\n"
            "• Ter conhecimento sobre as regras da cidade;\n"
            "• Ter conhecimentos básicos sobre FiveM;\n"
            "• Ser educado(a), ético(a), imparcial, atencioso(a), responsável e ter maturidade;\n\n"
            "Clique no botão abaixo para abrir seu formulário."
        ),
        color=discord.Color.blurple()
    )

    if BANNER_INICIO_URL:
        embed.set_image(url=BANNER_INICIO_URL)

    if LOGO_URL:
        embed.set_thumbnail(url=LOGO_URL)

    embed.set_footer(text="Boa sorte no recrutamento da staff!")

    await ctx.send(embed=embed, view=StartView())


@bot.command()
@commands.has_permissions(administrator=True)
async def enviar_painel(ctx):
    canal = bot.get_channel(CANAL_PAINEL_ID)
    if canal is None:
        await ctx.send("Canal do painel não encontrado.")
        return

    embed = discord.Embed(
        title="📋 Formulário Para Staff da Máfia RP📋",
        description=(
            "♛═════ 𝐑𝐞𝐪𝐮𝐢𝐬𝐢𝐭𝐨𝐬 𝐌𝐢́𝐧𝐢𝐦𝐨𝐬 ═════♛\n\n"
            "• Ter no mínimo 18 Anos de idade;\n"
            "• Ter no mínimo 1 meses de RP;\n"
            "• Ter responsabilidade e maturidade;\n"
            "• Ter conhecimento sobre as regras da cidade;\n"
            "• Ter conhecimentos básicos sobre FiveM;\n"
            "• Ser educado(a), ético(a), imparcial, atencioso(a), responsável e ter maturidade;\n\n"
            "Clique no botão abaixo para iniciar seu formulário."
        ),
        color=discord.Color.blurple()
    )

    if BANNER_INICIO_URL:
        embed.set_image(url=BANNER_INICIO_URL)

    if LOGO_URL:
        embed.set_thumbnail(url=LOGO_URL)

    embed.set_footer(text="Sistema oficial de recrutamento")

    await canal.send(embed=embed, view=StartView())
    await ctx.send("Painel enviado com sucesso.")


@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")


bot.run(TOKEN)