When(/^I do transfer (\d+) (\w+) from accountname: (\w+) to address: (\w+)$/) do |amount, symbol, account, address|
    @current_actor.node.exec 'wallet_transfer_asset_to_address', amount, symbol, account, @addresses[address]
end

When(/^I do transfer (\d+) (\w+) from address: (\w+) to account: (\w+)$/) do |amount, symbol, address, account|
    @current_actor.node.exec 'wallet_withdraw_from_address', amount, symbol, @addresses[address], account
end

When(/^I do transfer (\d+) (\w+) from address: (\w+) to public account for: (\w+)$/) do |amount, symbol, from_addr, account|
    to_addr = @current_actor.node.exec 'wallet_get_account_public_address', account
    puts "from " + @addresses[from_addr]
    puts "to " + to_addr
    @current_actor.node.exec 'wallet_withdraw_from_address', amount, symbol, @addresses[from_addr], to_addr
end

When(/^I do offline transfer (\d+) (\w+) from address: (\w+) to address: (\w+) as (\w+)$/) do |amount, symbol, from, to, builder_id|
    @addresses[builder_id] = @current_actor.node.exec 'wallet_withdraw_from_address', amount, symbol, @addresses[from], @addresses[to]
end