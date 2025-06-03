            # Initialise level 1
            ingame_level_data.Ingame_data["current_player_health"] = config.Level_preset[level]["player_health"]
            ingame_level_data.Ingame_data["current_player_currency"] = config.Level_preset[level]["player_currency"]
            generate_enemies(level)
            generate_button(level)
            generate_music(level)

            global background
            background = pygame.transform.scale_by(config.Level_preset[level]["background"], ingame_level_data.Ingame_data["resize_factor"])

            # The enemies spawn relative to when the
            global time_level_init
            time_level_init = pygame.time.get_ticks()/1000

            ingame_level_data.Ingame_data["held_item"] = None
            ingame_level_data.Ingame_data["checkpoints"] = config.Level_preset[level]["checkpoints"]
            ingame_level_data.Ingame_data["enemy_count"] = config.Level_preset[level]["enemy_count"]