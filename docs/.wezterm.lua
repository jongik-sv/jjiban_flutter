local wezterm = require 'wezterm'
local config = wezterm.config_builder()
local mux = wezterm.mux

-- ============================================
-- 0. Startup Layout (4-Pane Split)
-- ============================================

-- 멀티플렉서 서버 시작 시 4분할 레이아웃 생성
-- (mux-startup: 서버가 처음 시작될 때만 실행)
wezterm.on('mux-startup', function()
  -- 첫 번째 윈도우와 탭 생성
  local tab, pane, window = mux.spawn_window {}

  -- 레이아웃:
  -- +-------+-------+
  -- |   0   |   1   |
  -- +-------+-------+
  -- |   2   |   3   |
  -- +-------+-------+

  -- 오른쪽으로 분할 (pane 1 생성)
  local pane_right = pane:split { direction = 'Right' }

  -- 왼쪽 pane(0)을 아래로 분할 (pane 2 생성)
  local pane_bottom_left = pane:split { direction = 'Bottom' }

  -- 오른쪽 pane(1)을 아래로 분할 (pane 3 생성)
  local pane_bottom_right = pane_right:split { direction = 'Bottom' }

  -- 첫 번째 pane에 포커스
  pane:activate()
end)

-- 초기 윈도우 크기: 80x25 * 4 panes = 160 cols x 50 rows
config.initial_cols = 162  -- 80*2 + 분할선 여유
config.initial_rows = 52   -- 25*2 + 분할선 여유

-- ============================================
-- 1. Multiplexer (Unix Domain) Configuration
-- ============================================

-- Unix domain for multiplexer functionality (works on Windows too)
config.unix_domains = {
  {
    name = 'unix',
    -- Socket path (default: auto-generated in user's runtime dir)
    -- socket_path = 'C:/Users/sviso/.local/share/wezterm/sock',
  },
}

-- Auto-connect to unix domain on startup (like tmux attach)
-- Comment this out if you prefer manual connection
config.default_gui_startup_args = { 'connect', 'unix' }

-- ============================================
-- 2. Basic Appearance
-- ============================================

-- Color scheme
config.color_scheme = 'Tokyo Night'

-- Font settings
config.font = wezterm.font('JetBrains Mono', { weight = 'Medium' })
config.font_size = 11.0

-- Window settings
config.window_background_opacity = 0.95
config.window_padding = {
  left = 5,
  right = 5,
  top = 5,
  bottom = 5,
}

-- Tab bar
config.use_fancy_tab_bar = false
config.hide_tab_bar_if_only_one_tab = false
config.tab_bar_at_bottom = true

-- ============================================
-- 3. Key Bindings (tmux-like)
-- ============================================

-- Leader key: CTRL+A (like tmux with prefix)
config.leader = { key = 'a', mods = 'CTRL', timeout_milliseconds = 1000 }

config.keys = {-- Pane splitting (Leader + | or -)
  {
    key = '|',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.SplitHorizontal { domain = 'CurrentPaneDomain'},
  },
  {
    key = '-',
    mods = 'LEADER',
    action = wezterm.action.SplitVertical { domain = 'CurrentPaneDomain' },
  },

  -- Pane navigation (Leader + h/j/k/l)
  {
    key = 'h',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Left',
  },
  {
    key = 'j',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Down',
  },
  {
    key = 'k',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Up',
  },
  {
    key = 'l',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Right',
  },

  -- Pane resize (Leader + H/J/K/L)
  {
    key = 'H',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Left', 5 },
  },
  {
    key = 'J',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Down', 5 },
  },
  {
    key = 'K',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Up', 5 },
  },
  {
    key = 'L',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Right', 5 },
  },

  -- New tab (Leader + c)
  {
    key = 'c',
    mods = 'LEADER',
    action = wezterm.action.SpawnTab 'CurrentPaneDomain',
  },

  -- Close pane (Leader + x)
  {
    key = 'x',
    mods = 'LEADER',
    action = wezterm.action.CloseCurrentPane { confirm = true },
  },

  -- Zoom pane toggle (Leader + z)
  {
    key = 'z',
    mods = 'LEADER',
    action = wezterm.action.TogglePaneZoomState,
  },

  -- Tab navigation (Leader + number)
  { key = '1', mods = 'LEADER', action = wezterm.action.ActivateTab(0) },
  { key = '2', mods = 'LEADER', action = wezterm.action.ActivateTab(1) },
  { key = '3', mods = 'LEADER', action = wezterm.action.ActivateTab(2) },
  { key = '4', mods = 'LEADER', action = wezterm.action.ActivateTab(3) },
  { key = '5', mods = 'LEADER', action = wezterm.action.ActivateTab(4) },

  -- Next/Previous tab (Leader + n/p)
  { key = 'n', mods = 'LEADER', action = wezterm.action.ActivateTabRelative(1) },
  { key = 'p', mods = 'LEADER', action = wezterm.action.ActivateTabRelative(-1) },

  -- Copy mode (Leader + [)
  {
    key = '[',
    mods = 'LEADER',
    action = wezterm.action.ActivateCopyMode,
  },

  -- Show launcher (Leader + s)
  {
    key = 's',
    mods = 'LEADER',
    action = wezterm.action.ShowLauncherArgs { flags = 'FUZZY|WORKSPACES' },
  },

  -- Rename tab (Leader + ,)
  {
    key = ',',
    mods = 'LEADER',
    action = wezterm.action.PromptInputLine {
      description = 'Enter new tab name:',
      action = wezterm.action_callback(function(window, pane, line)
        if line then
          window:active_tab():set_title(line)
        end
      end),
    },
  },
}

-- ============================================
-- 4. Mouse Bindings
-- ============================================

config.mouse_bindings = {
  -- Right click paste
  {
    event = { Down = { streak = 1, button = 'Right' } },
    mods = 'NONE',
    action = wezterm.action.PasteFrom 'Clipboard',
  },
}

-- ============================================
-- 5. Misc Settings
-- ============================================

-- Scrollback
config.scrollback_lines = 10000

-- Bell
config.audible_bell = 'Disabled'

-- Cursor
config.default_cursor_style = 'BlinkingBar'
config.cursor_blink_rate = 500
config.enable_csi_u_key_encoding = false
-- Windows specific
-- PowerShell 7 (pwsh) + UTF-8
-- config.default_prog = { 'pwsh.exe', '-NoLogo', '-Command', '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; claude --dangerously-skip-permissions' }
-- Windows PowerShell 5.1
-- config.default_prog = { 'powershell.exe', '-NoLogo', '-Command', '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; claude --dangerously-skip-permissions' }
config.default_prog = { 'cmd.exe', "/k", "chcp 65001 && claude --dangerously-skip-permissions" }           -- CMDs 는 chcp 65001로 UTF-8 설정
-- config.default_prog = { 'wsl.exe' }           -- WSL
-- config.default_prog = { 'claude --dangerously-skip-permissions' }  -- Claude Code

-- Windows stdin 호환성
config.allow_win32_input_mode = true

-- -- 기본 쉘 UTF-8 강제
-- if wezterm.target_triple == 'x86_64-pc-windows-msvc' then
--   config.default_prog = { 'powershell.exe', '-NoLogo', '-ExecutionPolicy', 'Bypass', '-Command', 'chcp 65001' }
-- end

return config
