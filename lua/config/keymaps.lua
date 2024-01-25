local keymap = vim.keymap

local opts = { noremap = true, silent = true }

-- Naevagacao de pastas
keymap.set("n", "<leader>m", ":NvimTreeFocus<CR>", opts) -- Mover cursor para pasta
keymap.set("n", "<leader>f", ":NvimTreeToggle<CR>", opts) -- Abrir / Fechar pasta

-- Navegacao entre janelas
keymap.set("n", "<C-h>", "<C-w>h", opts) -- Mover para esquerda
keymap.set("n", "<C-j>", "<C-w>j", opts) -- Mover para baixo
keymap.set("n", "<C-k>", "<C-w>k", opts) -- Mover para cima
keymap.set("n", "<C-l>", "<C-w>l", opts) -- Mover para direita

-- Gerenciamneto de janelas
keymap.set("n", "<leader>sv", ":vsplit<CR>", opts) -- dividir verticalmente
keymap.set("n", "<leader>sh", ":split<CR>", opts) -- dividir horizontalmente
keymap.set("n", "<leader>sm", ":MaximizerToggle<CR>", opts) -- Maximizar ou minimizar

-- Identacao
keymap.set("v", "<", "<gv")
keymap.set("v", ">", ">gv")

-- Comentarios
vim.api.nvim_set_keymap("n", "<C-_>", "gcc", { noremap = false })
vim.api.nvim_set_keymap("v", "<C-_>", "gcc", { noremap = false })
