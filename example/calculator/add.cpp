/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

class add : public SST::Component {
public:
    add(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_add_opand1(SST::Event*);

    void handle_add_opand2(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(add, // class
                               "calculator", // element library
                               "add", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS({"add_opand1", "Operand 1", {"sst.Interfaces.StringEvent"}},
                           {"add_opand2", "Operand 2", {"sst.Interfaces.StringEvent"}},
                           {"sum_dout", "Sum", {"sst.Interfaces.StringEvent"}},
                           {"add_of_dout", "Overflow", {"sst.Interfaces.StringEvent"}}, )

private:
    std::string m_clock;
    SST::Link *add_opand1_link, *add_opand2_link, *sum_dout_link, *add_of_dout_link;

    int add_opand1, add_opand2;
    // SST parameters
    SST::Output m_output;
};

add::add(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id)
    , m_clock(params.find<std::string>("clock", ""))
    , sum_dout_link(configureLink("sum_dout"))
    , add_of_dout_link(configureLink("add_of_dout"))
    , add_opand1_link(
          configureLink("add_opand1", new SST::Event::Handler<add>(this, &add::handle_add_opand1)))
    , add_opand2_link(configureLink("add_opand2",
                                    new SST::Event::Handler<add>(this, &add::handle_add_opand2))) {
    m_output.init("\033[34mparent-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    if(!(add_opand1_link && add_opand2_link && sum_dout_link && add_of_dout_link)) {
        m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }

    registerClock(m_clock, new SST::Clock::Handler<add>(this, &add::tick));

    // Tell SST to wait until we authorize it to exit
    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();
}

void add::setup() {
    m_output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void add::finish() {
    m_output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
}

void add::handle_add_opand1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if(se) {
        m_output.verbose(CALL_INFO, 1, 0, "OPAND1 %s...\n", se->getString().c_str());
        add_opand1 = std::stoi(se->getString());
    }
    delete ev;
}

void add::handle_add_opand2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if(se) {
        m_output.verbose(CALL_INFO, 1, 0, "OPAND2 %s...\n", se->getString().c_str());
        add_opand2 = std::stoi(se->getString());
    }
    delete ev;
}

bool add::tick(SST::Cycle_t current_cycle) {

    if(add_opand1 && add_opand2) {
        std::string sum_dout = std::to_string(add_opand1 + add_opand2);
        std::cout << "SUKM IS " << sum_dout << '\n';
        sum_dout_link->send(new SST::Interfaces::StringEvent(sum_dout));
        add_of_dout_link->send(new SST::Interfaces::StringEvent("0"));
    }
    return false;
}
