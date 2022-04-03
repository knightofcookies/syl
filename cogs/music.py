import discordSuperUtils
import discord
import config
from discordSuperUtils import MusicManager
from discord.ext import commands
from discord import Colour
from tools.tools import send_embed

wcm = "✅"
color = Colour.blue()

syl_db = config.syl_db

# Adding Collections
user_playlist_count_col = syl_db["user_playlist_count"]
playlist_col = syl_db["playlists"]


class Music(commands.Cog, discordSuperUtils.CogManager.Cog, name="Music"):
    """Commands for music playback"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client_id = config.spotifyClientId
        self.client_secret = config.spotifyClientSecret
        self.musicmanager = MusicManager(bot,
                                         spotify_support=True,
                                         inactivity_timeout=300,
                                         minimum_users=1,
                                         client_id=self.client_id,
                                         client_secret=self.client_secret,
                                         default_volume=100)

        super().__init__()

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_music_error(self, ctx, error):
        raise error

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx):
        newEmbed = discord.Embed(
            description='The queue has ended.', color=color)
        await send_embed(ctx, newEmbed)

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
        newEmbed = discord.Embed(
            description='I left the voice channel due to inactivity.',
            color=color)
        await send_embed(ctx, newEmbed)

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_play(self, ctx, player):
        newEmbed = discord.Embed(
            description=f"Now playing: {player.title}", color=color)
        await send_embed(ctx, newEmbed)

    @commands.command(aliases=['leave', 'disconnect'])
    async def dc(self, ctx):
        """Leaves the voice channel"""

        try:
            if await self.musicmanager.leave(ctx):
                await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description=('I couldn\'t leave the voice channel!'
                             ' Please check if I\'m in a voice channel '
                             'before using this command.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['now_playing', 'nowplaying'])
    async def np(self, ctx):
        """Displays info about the current track"""

        try:
            if player := await self.musicmanager.now_playing(ctx):
                duration_played = round(await self.musicmanager
                                        .get_player_played_duration(ctx,
                                                                    player)
                                        )
                newEmbed = discord.Embed(
                    description=(f"Currently playing: {player}"),
                    color=color)
                temp = f"{duration_played}s played out of {player.duration}s"
                newEmbed.set_footer(text=temp)
                await send_embed(ctx, newEmbed)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description="I don't think I'm playing anything right now",
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def join(self, ctx):
        """Joins the voice channel"""

        try:
            if await self.musicmanager.join(ctx):
                await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error',
                description='I couldn\'t join the voice channel',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str):
        """Plays a track, supports youtube and spotify"""

        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await self.musicmanager.join(ctx)

        players = await self.musicmanager.create_player(query, ctx.author)

        if players:
            bool_1 = await self.musicmanager.queue_add(players=players,
                                                       ctx=ctx)
            bool_2 = await self.musicmanager.play(ctx)
            if bool_1 and not bool_2:
                if len(players) == 1:
                    newEmbed = discord.Embed(
                        description=f'{players[0].title} added to queue.',
                        colour=color)
                else:
                    newEmbed = discord.Embed(
                        description=('Your playlist has been'
                                     ' added to the queue.'),
                        color=color)

                await send_embed(ctx, newEmbed)

        else:
            newEmbed = discord.Embed(
                description='Query not found.', color=color)
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        try:
            await self.musicmanager.volume(ctx, volume)
            await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('This command can only be used '
                             'if the bot is playing something'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def looptrack(self, ctx):
        """Toggles loop for the current track"""

        try:
            is_loop = await self.musicmanager.loop(ctx)
            await ctx.message.add_reaction(wcm)
            newEmbed = discord.Embed(
                description=f"Looping toggled to {is_loop}", color=color)
            await send_embed(ctx, newEmbed)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error toggling loop',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Displays the queue"""

        try:
            formatted_queue = [
                f"Title: {x.title}\nRequester: {x.requester.mention}"
                for x in (await self.musicmanager.get_queue(ctx)).queue
                ]

            embeds = discordSuperUtils.generate_embeds(
                formatted_queue,
                "Queue",
                f"Now Playing: {await self.musicmanager.now_playing(ctx)}",
                25,
                string_format="{}",
                color=color,
                )

            page_manager = discordSuperUtils.PageManager(
                ctx, embeds, public=True)
            await page_manager.run()

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error trying to get the queue',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['yeet', 'r'])
    async def remove(self, ctx, index: int):
        """Removes an item from the queue at the specified index"""

        try:
            await self.musicmanager.queue_remove(ctx, index - 1)
            await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='I couldn\'t remove that item from the queue',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def lyrics(self, ctx, *, query: str = None):
        """Gets the lyrics for the current song or search query"""

        try:
            if response := await self.musicmanager.lyrics(ctx, query):
                title, author, query_lyrics = response

                splitted = query_lyrics.split("\n")
                res = []
                current = ""
                for i, split in enumerate(splitted):
                    bool_1 = len(splitted) <= i + 1
                    bool_2 = len(current) + len(splitted[i + 1]) > 1024
                    if bool_1 or bool_2:
                        res.append(current)
                        current = ""
                        continue
                    current += split + "\n"
                page_manager = discordSuperUtils.PageManager(
                    ctx,
                    [
                        discord.Embed(
                            title=(f"Lyrics for '{title}' by '{author}', "
                                   f"(Page {i + 1}/{len(res)})"),
                            description=x,
                            colour=color
                        )
                        for i, x in enumerate(res)
                    ],
                    public=True,
                )
                await page_manager.run()

            else:
                newEmbed = discord.Embed(
                    description='No lyrics found', color=color)
                await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error processing your request',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def pause(self, ctx):
        """Pauses the player"""

        try:
            x = await self.musicmanager.pause(ctx)
            if x:
                await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='I couldn\'t pause the player',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['next'])
    async def skip(self, ctx, index: int):
        """Skips the player to the specified index or the next song"""

        try:
            await self.musicmanager.skip(ctx, index)
            await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='I couldn\'t skip the player to that index',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def loopqueue(self, ctx):
        """Toggles loop for the current queue"""

        try:
            is_loop = await self.musicmanager.queueloop(ctx)
            await ctx.message.add_reaction(wcm)
            newEmbed = discord.Embed(
                description=f"Looping toggled to {is_loop}", color=color)
            await send_embed(ctx, newEmbed)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error toggling loop',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def shuffle(self, ctx):
        """Toggles shuffle"""

        try:
            is_shuffle = await self.musicmanager.shuffle(ctx)
            if is_shuffle:
                pass
            else:
                await self.musicmanager.shuffle(ctx)
                newEmbed = discord.Embed(
                    description='I shuffled the queue.',
                    color=color)
                await send_embed(ctx, newEmbed)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error toggling shuffle',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def autoplay(self, ctx):
        """Toggles autoplay"""

        try:
            is_autoplay = await self.musicmanager.autoplay(ctx)
            newEmbed = discord.Embed(
                description=f'Autoplay toggled to {is_autoplay}', color=color)
            await send_embed(ctx, newEmbed)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error toggling autoplay',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def history(self, ctx):
        """Displays listening history"""

        try:
            formatted_history = [
                f"Title: '{x.title}'\nRequester: {x.requester.mention}"
                for x in (await self.musicmanager.get_queue(ctx)).history
            ]

            embeds = discordSuperUtils.generate_embeds(
                formatted_history,
                "Song History",
                "Shows all played songs",
                25,
                string_format="{}",
                color=color,
            )

            page_manager = discordSuperUtils.PageManager(
                ctx, embeds, public=True)
            await page_manager.run()

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error processing your request',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['loopstatus, loop_status'])
    async def ls(self, ctx):
        """Shows loop status"""

        try:
            if queue := await self.musicmanager.get_queue(ctx):
                loop = queue.loop
                loop_status = None

                if loop == discordSuperUtils.Loops.LOOP:
                    loop_status = "Looping enabled."

                elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
                    loop_status = "Queue looping enabled."

                elif loop == discordSuperUtils.Loops.NO_LOOP:
                    loop_status = "No loop enabled."

                if loop_status:
                    newEmbed = discord.Embed(
                        description=loop_status, color=color)

                await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description='There was an error processing your request',
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command()
    async def stop(self, ctx):
        """Stops playback and clears the queue"""

        try:
            await self.musicmanager.cleanup(guild=ctx.guild, voice_client=None)
            ctx.voice_client.stop()
            await ctx.message.add_reaction(wcm)
        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('There was an error clearing '
                             'the queue and stopping playback.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['saveplaylist',
                               'savequeue',
                               'saveasplaylist',
                               'save_as_playlist',
                               'saveas_playlist'])
    async def save_queue(self, ctx, *, args=None):
        """Saves the current queue as a custom playlist with a name"""

        # Get the number of playlists the user has saved
        # If the user has a playlist saved
        usercountdoc = user_playlist_count_col.find_one(
            {"id": str(ctx.author.id)})

        if usercountdoc is not None:

            usercountdoc = user_playlist_count_col.find_one(
                {"id": str(ctx.author.id)})
            usercount = usercountdoc["count"]
            if not usercount >= 100:
                id = str(ctx.author.id)
                count = usercount + 1
                user_playlist_count_col.update_one({"id": id}, {
                                                   "$set": {"count": count}})
                playlist_limit_permit = True
            else:
                newEmbed = discord.Embed(
                    title='Playlist Limit Reached',
                    description='You can\'t create more than 99 playlists!',
                    color=color)
                await send_embed(ctx, newEmbed)
                playlist_limit_permit = False

        # If this is the user's first saved playlist
        else:
            user_playlist_count_col.insert_one(
                {'id': str(ctx.author.id), 'count': 1})
            usercount = 0
            playlist_limit_permit = True

        if args is None:
            args = f"Playlist{str(usercount + 1)}"

        if playlist_limit_permit:
            try:
                # Creating a new playlist in the database
                new_playlist_id = str(((ctx.author.id)*100) + usercount + 1)
                playlist_col.insert_one(
                    {'name': args, 'id': new_playlist_id})

                # Adding each track to the playlist
                i = 0
                for track in (await self.musicmanager.get_queue(ctx)).queue:
                    i = i + 1
                    playlist_col.update_one({'id': new_playlist_id}, {
                                            "$set": {f'song{i}': track.title}})

                # Updating the length of the playlist in the database
                playlist_col.update_one({'id': new_playlist_id}, {
                                        "$set": {'length': i}})

                newEmbed = discord.Embed(
                    title='Success!',
                    description=('I created a new playlist for you '
                                 f'titled `{args}` '
                                 'with the current queue.'),
                    color=color)

            except Exception as e:
                newEmbed = discord.Embed(
                    title='Error!',
                    description=('I was unable to create a playlist with this '
                                 'queue!\n Note that this command can be used'
                                 ' only when the queue isn\'t empty.'),
                    color=color)
                newEmbed.set_footer(text=str(e))

            # Send a response
            await send_embed(ctx, newEmbed)

        else:
            pass

    @commands.command(aliases=['show_playlists',
                               'view_playlists',
                               'my_playlists',
                               'showplaylists',
                               'viewplaylists',
                               'myplaylists',
                               'listplaylists'])
    async def list_playlists(self, ctx):
        """Lists your saved playlists"""

        # Fetch the number of playlists the user has made
        try:
            user_playlist_count_doc = user_playlist_count_col.find_one(
                {'id': str(ctx.author.id)})
            if user_playlist_count_doc is None:
                newEmbed = discord.Embed(
                    description='You haven\'t created any playlists yet.',
                    color=color)
                await send_embed(ctx, newEmbed)
                user_playlist_count = None
            else:
                user_playlist_count = user_playlist_count_doc['count']

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('There was an error while I was trying to'
                             ' check if you\'ve created any playlists'),
                color=color
            )
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

        # Printing the list of playlists
        try:
            playlists_list = []
            if user_playlist_count is not None:
                if user_playlist_count != 1:
                    for i in range(1, user_playlist_count + 1):
                        playlist_doc = playlist_col.find_one(
                            {'id': str(((ctx.author.id)*100)+i)})
                        playlists_list.append(playlist_doc['name'])
                else:
                    playlist_doc = playlist_col.find_one(
                        {'id': str(((ctx.author.id)*100)+1)})
                    playlists_list.append(playlist_doc['name'])

                formatted_playlist_list = [
                    f"`{temp}`"
                    for temp in playlists_list
                ]

                newEmbed = discordSuperUtils.generate_embeds(
                    formatted_playlist_list,
                    "Your Playlists",
                    '',
                    25,
                    string_format="{}",
                    color=color,
                )

                page_manager = discordSuperUtils.PageManager(
                    ctx, newEmbed, public=False)
                await page_manager.run()

            else:
                pass

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('There was an error while I was trying to'
                             ' print a list of your playlists'),
                color=color
            )
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['deleteplaylist',
                               'playlist_delete',
                               'playlistdelete'])
    async def delete_playlist(self, ctx, *, playlist_id: int):
        """Deletes the playlist with the index from list_playlists"""

        try:
            if playlist_id is not None:
                playlist_col.delete_one(
                    {'id': str(((ctx.author.id)*100)+playlist_id)})
                newEmbed = discord.Embed(
                    description='I deleted that playlist!', color=color)
                temp_doc = user_playlist_count_col.find_one(
                    {'id': str(ctx.author.id)})
                if playlist_id == 1 and temp_doc['count'] == 1:
                    user_playlist_count_col.delete_one(
                        {'id': str(ctx.author.id)})
                else:
                    temp_doc = user_playlist_count_col.find_one(
                        {'id': str(ctx.author.id)})
                    t_count = temp_doc['count'] - 1
                    user_playlist_count_col.update_one(
                        {'id': temp_doc['id']}, {"$set": {'count': t_count}})

                    # Updating ids of the following playlists
                    usercountdoc = user_playlist_count_col.find_one(
                        {'id': str(ctx.author.id)})
                    usercount = usercountdoc['count']

                    if playlist_id < usercount:
                        for i in range(id, usercount + 1):
                            playlist_doc = playlist_col.find_one(
                                {'id': str(((ctx.author.id)*100)+i)})
                            t_p_id = str((((ctx.author.id)*100)+i)-1)
                            p_id = playlist_doc["_id"]
                            playlist_col.update_one({'_id': p_id}, {
                                                    "$set": {'id': t_p_id}})

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('I couldn\'t delete that playlist. '
                             'Please check if you\'ve entered'
                             'the correct index.'))
            newEmbed.set_footer(text=str(e))

        await send_embed(ctx, newEmbed)

    @commands.command(aliases=['show_playlist',
                               'view_playlist',
                               'list_playlist'])
    async def playlist(self, ctx, playlist_id: int):
        """Lists all the songs in the given playlist"""

        try:
            playlist_doc = playlist_col.find_one(
                {'id': str(((ctx.author.id)*100)+playlist_id)})

            songs = []
            for i in range(1, playlist_doc['length'] + 1):
                index = f'song{i}'
                songs.append(playlist_doc[index])

            formatted_songs_list = [
                f"`{temp}`"
                for temp in songs
            ]

            newEmbed = discordSuperUtils.generate_embeds(
                formatted_songs_list,
                playlist_doc['name'],
                '',
                25,
                string_format="{}",
                color=color,
            )

            page_manager = discordSuperUtils.PageManager(
                ctx, newEmbed, public=False)
            await page_manager.run()

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('I couldn\'t list that playlist.'
                             ' Please check if you\'ve entered the '
                             'correct index.'))
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)

    @commands.command(aliases=['ppl',
                               'playfromplaylist',
                               'play_from_playlist',
                               'playplaylist'])
    async def play_playlist(self, ctx, playlist_id: int):
        """Adds the playist with the given id to the queue"""

        try:

            if not ctx.voice_client or not ctx.voice_client.is_connected():
                await self.musicmanager.join(ctx)

            playlist_doc = playlist_col.find_one(
                {'id': str(((ctx.author.id)*100)+playlist_id)})

            for i in range(1, (playlist_doc['length'] + 1)):
                index = f"song{i}"
                j = playlist_doc[index]
                players = await self.musicmanager.create_player(j,
                                                                ctx.author)
                if players:
                    await self.musicmanager.queue_add(players=players, ctx=ctx)
                    await self.musicmanager.play(ctx)

            newEmbed = discord.Embed(
                description='Playlist added to queue.', colour=color)
            await send_embed(ctx, newEmbed)

        except Exception as e:
            newEmbed = discord.Embed(
                title='Error!',
                description=('I couldn\'t play that playlist. '
                             'Please check if you\'ve'
                             ' entered the correct index.'),
                color=color)
            newEmbed.set_footer(text=str(e))
            await send_embed(ctx, newEmbed)


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
